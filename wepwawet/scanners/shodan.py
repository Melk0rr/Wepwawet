import shodan

sho_props = ["city", "country_name", "domains", "isp", "org", "ports"]
sho_data_props = ["product"]

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

    sho_base = filter_dictionary_properties(sho_req, sho_props)
    sho_data = filter_nested_properties(sho_req.get("data", []), sho_data_props)

    self.urls.append({
      **target,
      **sho_base,
      **sho_data,
      "error": err_msg
    })


def filter_dictionary_properties(dictionary, properties):
  return { x: dictionary.get(x, "") for x in properties }

def filter_nested_properties(dictionaries, properties):
  return { p: [ d.get(p, "") for d in dictionaries ] for p in properties }