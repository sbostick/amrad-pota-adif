"""
ActivationLog() represents one POTA activation.

Intended use for ActivationLog class:
1. Load QSO records from a yaml input file to python native data structures
2. Augment the in-memory QSO records with QRZ lookups (by callsign)
3. Write debug.yaml file representing the full/complete QSO data set
4. Write an ADIF file for upload to https://pota.app
"""
import os
import datetime
from dateutil.tz import tzlocal, UTC
import yaml
import logging
import xml.etree.ElementTree as ET
import config
import adif
import qrz


class ActivationLog():
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

            # APPLY DEFAULTS IF NEEDED
            defaults = self.rawdata.get('QSO_DEFAULTS')
            for qso_field in defaults.keys():
                qso_value = str(entry.get(qso_field, ""))
                if not len(qso_value):
                    entry[qso_field] = defaults.get(qso_field, "")

            # REPLACE NULL WITH EMPTY STRING
            for qso_field in entry.keys():
                qso_value = str(entry.get(qso_field))
                if not len(qso_value):
                    entry[qso_field] = ''

    def write_yaml(self, outfile):
        try:
            with open(outfile, 'w', encoding='utf-8') as fout:
                fout.write(yaml.dump(self.rawdata))
        except yaml.scanner.ScannerError as err:
            logging.error(f'{outfile} failed yaml validation')
            raise err

    def write_adi(self, outfile):
        now_utc = datetime.datetime.now(UTC)
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
