import config
import requests
import xml.etree.ElementTree as ET
import logging


class Client():
    def __init__(self, agent, endpoint, username, password):
        auth_url = (f"{endpoint}/?"
                    f"agent={agent};"
                    f"username={username};"
                    f"password={password}")

        logging.debug("QRZ client init")
        result = requests.get(url=auth_url, timeout=5)
        assert result.status_code == 200

        root = ET.fromstring(result.text)
        # ET.indent(root, space="  ", level=0)
        # ET.dump(root)
        session_key = root.find('./{*}Session/{*}Key')
        self.session_key = session_key.text

    def lookup(self, callsign):
        logging.debug("QRZ lookup")
        lookup_url = (f"{config.QRZ_ENDPOINT}/?"
                      f"s={self.session_key};"
                      f"callsign={callsign}")
        result = requests.get(url=lookup_url, timeout=5)
        assert result.status_code == 200
        return result.text
