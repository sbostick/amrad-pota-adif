"""
Use for loading secrets from GNU Pass CLI.
"""
import subprocess
import json
import yaml


class Secret(object):
  def __init__(self, ident):
    command = ["pass", "show", ident]
    self.result = subprocess.run(command, capture_output=True)
    self.payload = self.result.stdout.decode('utf-8').strip()

  def __str__(self):
    return str(self.payload)

  def decode_json(self):
      return json.loads(self.payload)

  def decode_yaml(self):
      return yaml.loads(self.payload, Loader=yaml.SafeLoader)
