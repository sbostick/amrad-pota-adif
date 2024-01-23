import os
from datetime import datetime, timezone, timedelta
from dateutil.tz import tzlocal, UTC
import re
import yaml
import logging
import xml.etree.ElementTree as ET
import config
import utc_offset
import adif
import qrz


class ActivationLog():
    """
    Represents one POTA activation log (list of QSOs).

    Intended use:
    1. Load QSO records from a yaml input file to python native data structures
    2. Augment the in-memory QSO records with QRZ lookups (by callsign)
    3. Write debug.yaml file representing the full/complete QSO data set
    4. Write an ADIF file for upload to https://pota.app
    """
    def __init__(self):
        self.rawdata = {}
        self.qrz_client = qrz.Client(agent=config.QRZ_AGENT,
                                     endpoint=config.QRZ_ENDPOINT,
                                     username=config.QRZ_USER,
                                     password=config.QRZ_PASS)

    def read_yaml(self, infile):
        try:
            with open(infile, 'r', encoding='utf-8') as fin:
                self.rawdata = yaml.load(fin, Loader=yaml.SafeLoader)
        except yaml.scanner.ScannerError as err:
            logging.error(f'{infile} failed yaml validation')
            raise err

    def apply_qso_defaults(self):
        for idx, entry in enumerate(self.rawdata.get('QSO_LOG')):
            # Apply QSO_DEFAULTS to records
            defaults = self.rawdata.get('QSO_DEFAULTS')
            for qso_field in defaults.keys():
                qso_value = str(entry.get(qso_field, ""))
                if not len(qso_value):
                    entry[qso_field] = defaults.get(qso_field, "")

            # Replace null values with empty string
            for qso_field in entry.keys():
                qso_value = str(entry.get(qso_field))
                if not len(qso_value):
                    entry[qso_field] = ''

    def augment_with_qrz(self):
        for idx, entry in enumerate(self.rawdata.get('QSO_LOG')):
            callsign = entry['call']
            result = self.qrz_client.lookup(callsign)
            logging.debug(result)
            root = ET.fromstring(result)
            node = root.find('{*}Callsign')

            # QRZ FREE
            entry['country'] = node.find('{*}country').text
            entry['name'] = ' '.join([node.find('{*}fname').text,
                                      node.find('{*}name').text])
            entry['qth'] = node.find('{*}addr2').text
            entry['state'] = node.find('{*}state').text

            # QRZ SUBSCRIPTION REQUIRED
            # entry['grid'] = node.find('{*}grid').text
            # entry['addr1'] = node.find('{*}addr1').text
            # entry['zip'] = node.find('{*}zip').text


    # TODO(sbostick): using only (qso_date, time_on) for QSO records. Unsure
    # if (qso_date_off, time_off) are needed. POTA log submissions have been
    # successful with just the QSO start times.
    def convert_local_time_to_utc(self):
        offset = str(self.rawdata.get('INPUT_UTC_OFFSET', '0'))
        (utc_offset_hours, utc_offset_minutes) = utc_offset.parse(offset)
        utc_offset_str = utc_offset.to_string(offset)

        for idx, entry in enumerate(self.rawdata.get('QSO_LOG')):
            # Method 1 -- use timezone conversion method
            iso_date_string = (str(entry['qso_date']) + 'T'
                               + str(entry['time_on'])
                               + utc_offset_str)
            t_start = datetime.fromisoformat(iso_date_string)
            t_start = t_start.astimezone(tz=timezone.utc)
            logging.debug(t_start.strftime('%Y-%m-%d %H:%M:%S %z'))

            # Method 2 -- add timedelta to t_start
            ### t_start_2 = datetime.fromisoformat(iso_date_string)
            ### t_start_2 += timedelta(hours=(utc_offset_hours * -1),
            ###                        minutes=(utc_offset_minutes * -1))
            ### t_start_2 = t_start_2.replace(tzinfo=timezone.utc)
            ### logging.debug(t_start_2.strftime('%Y-%m-%d %H:%M:%S %z'))

            # Patch the record
            entry['time_on'] = t_start.strftime('%H%M')
            entry['qso_date'] = t_start.strftime('%Y%m%d')


    def write_yaml(self, outfile):
        try:
            with open(outfile, 'w', encoding='utf-8') as fout:
                fout.write(yaml.dump(self.rawdata))
        except yaml.scanner.ScannerError as err:
            logging.error(f'{outfile} failed yaml validation')
            raise err

    def write_adi(self, outfile):
        now_utc = datetime.now(UTC)
        generated_on = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

        try:
            with open(outfile, 'w', encoding='utf-8') as fout:
                fout.write(f"Generated on {generated_on}\n")
                fout.write(adif.field_with_newline('adif_ver',
                                                   config.ADIF_VER))
                fout.write(adif.field_with_newline('programid',
                                                   config.ADIF_PROGRAM_ID))
                fout.write(adif.field_with_newline('programversion',
                                                   config.ADIF_PROGRAM_VERSION))
                fout.write('<EOH>\n\n')

                for entry in self.rawdata.get('QSO_LOG'):
                    fout.write(adif.qso(entry))

        except yaml.scanner.ScannerError as err:
            logging.error(f'{outfile} failed yaml validation')
            raise err
