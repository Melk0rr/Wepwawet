from math import prod
import shodan

sho_props = ["city", "country_name", "domains", "isp", "org", "ports"]

"""
Main shodan function : Emit request to shodan via API
"""
def ask_shodan(self):
  print("Asking Shodan.io for additional information...")

  try:
    from wepwawet.API import SHODAN_KEY
  except:
    self.handle_exception(e, "Unable to import API key - make sure API.py exists!")
    return

  api = shodan.Shodan(SHODAN_KEY)

  for i in range(len(self.options["TARGET"])):
    target = self.options["TARGET"][i]
    sho_req = {}
    err_msg = ""

    try:
      # Asking shodan for the specified IP address
      if (target["ip"]):
        sho_req = api.host(target["ip"])

    except Exception as e:
      err_msg = e
      self.handle_exception(e, f"Error while retreiving shodan informations for {target['host']}")

    sho_base = filter_shodan_properties(sho_req, sho_props)
    sho_products = get_shodan_product(sho_req)

    self.urls.append({
      **target,
      **sho_base,
      **sho_products,
      "error": err_msg
    })


def filter_shodan_properties(shodan_req, properties):
  return { x: format_shodan_property(shodan_req.get(x, "")) for x in properties }

def format_shodan_property(shodan_property):
  return (', '.join("{}".format(n) for n in shodan_property)) if (type(shodan_property) is list) else shodan_property

def get_shodan_product(shodan_req):
  product_list = set()
  for d in (shodan_req.get("data", [])):
    product, port = d.get("product"), d.get("ports")

    if (product):
      product_str, port_str = product, f"({port})"
      product_list.add(f"{product_str}{port_str}")

  return { 'product': ', '.join(product_list) }
