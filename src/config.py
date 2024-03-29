# GENERAL USAGE
# -------------
# import config
# print(config.VAR)
# print(config.QRZ_CONF.field)

import os
from gnupass import Secret


########################################################################
#                SETTINGS PASSED FROM RUNTIME ENV                      #
########################################################################

APP_VERSION = os.environ.get('APP_VERSION')
BUILD_TIME = os.environ.get('BUILD_TIME')


########################################################################
#                         GENERAL CONFIG                               #
########################################################################

ADIF_VER = '3.0.5'
ADIF_PROGRAM_ID = 'KO6BGT'
ADIF_PROGRAM_VERSION = '0.0.3'


########################################################################
#                           QRZ CONFIG                                 #
########################################################################

QRZ_AGENT = f"{ADIF_PROGRAM_ID}v{ADIF_PROGRAM_VERSION}"
QRZ_ENDPOINT = "https://xmldata.qrz.com/xml/current"
QRZ_USER = Secret('qrz.com/KO6BGT.json').decode_json().get('username')
QRZ_PASS = Secret('qrz.com/KO6BGT.json').decode_json().get('password')

from dataclasses import dataclass
@dataclass
class QRZConfig:
    agent: str
    endpoint: str
    username: str = None
    password: str = None

QRZ_CONF = QRZConfig(QRZ_AGENT, QRZ_ENDPOINT, QRZ_USER, QRZ_PASS)
