import json

import requests


def geoloc(self, target):
  req_url = f"https://geolocation-db.com/jsonp/{target.get_ip()}"
  res = {}

  try:
    response = requests.get(req_url)
    res = response.content.decode()
    res = res.split("(")[1].strip(")")
    res = json.loads(res)

    target.set_geo_location(res["city"], res["country_name"])

  except Exception as e:
    self.handle_exception(
        e, f"Can't get geolocation for {target.get_domain()}. Make sure the target is accessible.")
