import shodan

from wepwawet.utils.color_print import ColorPrint

sho_props = ['city', 'country_name', 'domains', 'isp', 'org', 'ports']

'''
Main shodan function : Emit request to shodan via API
'''
def ask_shodan(self, target):
  print("Asking Shodan.io for additional information...")

  try:
    from wepwawet.API import SHODAN_KEY
  except:
    ColorPrint.red("Unable to import API key - make sure API.py exists!")
    return

  api = shodan.Shodan(SHODAN_KEY)

  try:
    # Asking shodan for the specified IP address
    if (target['ip']):
      sho_req = api.host(target['ip'])
      sho_less = {x:sho_req[x] for x in sho_props}

    res = { **target, **sho_less }
    self.urls.append(res)
  except Exception as e:
    self.handle_exception(e, "Error while retreiving shodan informations")