""" Shodan plugin which will interact with Shodan API to retreive ip data """
import shodan

from wepwawet.scanners.port import Port


def set_url_ports(target, shodan_request):
  """ Extract product list from ip ports data """

  # For each port json object, build a string with the port number and associated product
  for port_data in (shodan_request.get("data", [])):
    port = Port(int(port_data.get("port")), port_data.get("product"))
    target.append_open_port(port)


def ask_shodan(self, target, api):
  """ Main shodan function : Emit request to shodan via API """

  print("Asking Shodan.io...")
  api = shodan.Shodan(api)

  shodan_request = {}
  error_message = ""

  try:
    # Asking shodan for the specified IP address
    if target.get_ip():
      shodan_request = api.host(target.get_ip())

  except Exception as e:
    error_message = e
    self.handle_exception(
        e, f"Error while retreiving shodan informations for {target.get_domain()}: {e}")

  # Set URL geo location
  target.set_geo_location(shodan_request.get(
      "city", ""), shodan_request.get("country", ""))

  # Set URL related domain
  target.set_related_domains(shodan_request.get("domains", ""))

  # Set URL ports
  set_url_ports(target, shodan_request)

  shodan_res = {
      "isp": shodan_request.get("isp", ""),
      "org": shodan_request.get("org", ""),
      "error": error_message
  }

  return shodan_res
