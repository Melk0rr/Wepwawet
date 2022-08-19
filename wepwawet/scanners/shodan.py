""" Shodan plugin which will interact with Shodan API to retreive ip data """
from xml.dom import NotFoundErr
import shodan

sho_props = ["city", "country_name", "domains", "isp", "org", "ports"]


def ask_shodan(self):
  """ Main shodan function : Emit request to shodan via API """

  print("Asking Shodan.io for additional information...")

  try:
    from wepwawet.API import SHODAN_KEY
  except NotFoundErr as err:
    self.handle_exception(err, "Unable to import API key - make sure API.py exists!")
    return

  api = shodan.Shodan(SHODAN_KEY)

  for i in range(len(self.options["TARGET"])):
    target = self.options["TARGET"][i]
    sho_req = {}
    err_msg = ""

    try:
      # Asking shodan for the specified IP address
      if target["ip"]:
        sho_req = api.host(target["ip"])

    except Exception as err:
      err_msg = err
      self.handle_exception(err, f"Error while retreiving shodan informations for {target['host']}")

    sho_base = filter_shodan_properties(sho_req, sho_props)
    sho_products = get_shodan_product(sho_req)

    self.urls.append({
      **target,
      **sho_base,
      **sho_products,
      "error": err_msg
    })


def filter_shodan_properties(shodan_req, props):
  """ Filter shodan properties based on shop_props collection """
  return {x: format_shodan_property(shodan_req.get(x, "")) for x in props}


def format_shodan_property(prop):
  """ Format shodan property to a string and join values in case of a list """
  return (', '.join(f"{n}" for n in prop)) if isinstance(prop, list) else prop


def get_shodan_product(shodan_req):
  """ Extract product list from ip ports data """
  product_list = set()
  for port in (shodan_req.get("data", [])):
    product, port_num = port.get("product", ""), port.get("port", "")

    if product:
      product_str, port_str = product, f"({port_num})"
      product_list.add(f"{product_str}{port_str}")

  return {'product': ', '.join(product_list)}
