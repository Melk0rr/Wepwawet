import shodan

from wepwawet.utils.color_print import ColorPrint

sho_props = ['city', 'country_name', 'domains', 'isp', 'org', 'ports']

'''
Main shodan function : Emit request to shodan via API
'''
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
    sho_req = None
    
    try:
      # Asking shodan for the specified IP address
      if (target['ip']):
        sho_req = api.host(target['ip'])

    except Exception as e:
      self.handle_exception(e, f"Error while retreiving shodan informations for {target['host']}")

    sho_res = {x:sho_req[x] if sho_req else None for x in sho_props}
    self.urls.append({ **target, **sho_res })