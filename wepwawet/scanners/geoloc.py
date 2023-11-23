import json

import requests


def geoloc(self, target):
  req_url = f"http://ipwho.is/{target.get_ip()}"
  res = {}

  try:
    response = requests.get(req_url)
    res = response.content.decode()
    res = json.loads(res)

    target.set_geo_location(res.get("city", ""), res.get("country", ""))

  except Exception as e:
    self.handle_exception(
        e, f"Can't get geolocation for {target.get_domain()}. Make sure the target is accessible.")
