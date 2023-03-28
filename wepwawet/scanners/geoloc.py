import json

import requests


def geoloc(self, target):
  req_url = f"https://geolocation-db.com/{target.get_ip()}"
  res = {}

  try:
    response = requests.get(req_url)
    res = response.content.decode()
    res = res.split("(")[1].strip(")")
    res = json.loads(res)

  except Exception as e:
    self.handle_exception(
        e, f"Can't get geolocation for {target.get_ip()}. Make sure the target is accessible.")

  return res
