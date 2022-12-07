""" Shodan plugin which will interact with Shodan API to retreive ip data """
import shodan

shodan_properties = ["city", "country_name", "domains", "isp", "org", "ports"]

def format_shodan_property(property):
  """ Format shodan property to a string and join values in case of a list """
  return (', '.join(f"{n}" for n in property)) if isinstance(property, list) else property


def filter_shodan_properties(shodan_request):
  """ Filter shodan properties based on shop_props collection """
  return {x: format_shodan_property(shodan_request.get(x, "")) for x in shodan_properties}


def get_shodan_product(shodan_request):
  """ Extract product list from ip ports data """
  product_list = set()

  # For each port json object, build a string with the port number and associated product
  for port in (shodan_request.get("data", [])):
    product, port_number = port.get("product", ""), port.get("port", "")

    if product:
      product_str, port_str = product, f"({port_number})"
      product_list.add(f"{product_str}{port_str}")

  return {'product': ', '.join(product_list)}


def ask_shodan(self, target, api):
  """ Main shodan function : Emit request to shodan via API """

  print("Asking Shodan.io...")
  api = shodan.Shodan(api)

  shodan_request = {}
  error_message = ""

  print(f"\n* {target['host']} *")

  try:
    # Asking shodan for the specified IP address
    if target["ip"]:
      shodan_request = api.host(target["ip"])

  except Exception as e:
    error_message = e
    self.handle_exception(e, f"Error while retreiving shodan informations for {target['host']}")

  shodan_infos = {
    **filter_shodan_properties(shodan_request),
    **get_shodan_product(shodan_request),
    "error": error_message
  }

  print(f"Related domains: {shodan_infos['domains']}\nOpen ports: {shodan_infos['ports']}")
  return shodan_infos
