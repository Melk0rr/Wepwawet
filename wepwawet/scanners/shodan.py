""" Shodan plugin which will interact with Shodan API to retreive ip data """
import requests

from typing import Dict

from wepwawet.network import Port, URL


def set_url_ports(target: URL, shodan_request: Dict) -> None:
  """ Extract product list from ip ports data """
  port_list = shodan_request.get("ports", [])
  cpe_list = shodan_request.get("cpes", [])
  
  # For each port json object, build a string with the port number and associated product
  for i in range(len(port_list)):
    cpe = cpe_list[i] if i < len(cpe_list) else "Unknown"
    port = Port(int(port_list[i]), cpe)
    target.get_ip().append_open_port(port)


def ask_shodan(self, target: URL) -> Dict:
  """ Main shodan function : Emit request to shodan via API """

  print("Asking Shodan.io...")

  shodan_request = {}
  error_message = ""

  try:
    # Asking shodan for the specified IP address
    if target.get_ip():
      shodan_url = f"https://internetdb.shodan.io/{target.get_ip()}"
      shodan_request = requests.get(shodan_url).json()

  except Exception as e:
    error_message = e
    self.handle_exception(
        e, f"Error while retreiving shodan informations for {target.get_domain()}: {e}")

  # Set URL related domain
  target.set_related_domains(shodan_request.get("hostnames", ""))

  # Set URL ports
  set_url_ports(target, shodan_request)

  shodan_res = {
    "isp": shodan_request.get("isp", ""),
    "org": shodan_request.get("org", ""),
    "error": error_message
  }

  return shodan_res
