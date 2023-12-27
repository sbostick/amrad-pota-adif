import subprocess
import json
import yaml

GNU_PASS_BIN = "pass"


class Secret(object):
  def __init__(self, ident):
    command = [GNU_PASS_BIN, "show", ident]
    self.result = subprocess.run(command, capture_output=True)
    self.payload = self.result.stdout.decode('utf-8').strip()

  def __str__(self):
    return str(self.payload)

  def decode_json(self):
      return json.loads(self.payload)

  def decode_yaml(self):
      return yaml.loads(self.payload, Loader=yaml.SafeLoader)
