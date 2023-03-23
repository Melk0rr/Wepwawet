import json

import requests


def geoloc(self, ip):
  req_url = f"https://geolocation-db.com/jsonp/{ip}"
  res = {}

  try:
    response = requests.get(req_url)
    res = response.content.decode()
    res = res.split("(")[1].strip(")")
    res = json.loads(res)
  
  except Exception as e:
    self.handle_exception(
        e, f"Error while requesting {ip}. Make sure the target is accessible")

  return res