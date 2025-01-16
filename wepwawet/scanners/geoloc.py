import json
import requests

from wepwawet.utils.color_print import ColorPrint

def geoloc(self, target: "URL") -> None:
  if target.get_ip() is None:
    ColorPrint.red(f"No IP address to geolocate for {target}")
    return

  req_url = f"http://ipwho.is/{target.get_ip()}"
  res = {}

  print(f"{target.get_domain()}, geo locating", end="...")
  try:
    response = requests.get(req_url)
    res = response.content.decode()
    res = json.loads(res)

    city = res.get("city", "")
    country = res.get("country", "")
    target.set_geo_location(city=city, country=country)

    if country:
      ColorPrint.green(f"Location found {city}, {country}")

    else:
      ColorPrint.red("Location not found")

  except Exception as e:
    self.handle_exception(
        e, f"Can't get geolocation for {target.get_domain()}. Make sure the target is accessible.")
