import shodan

from utils.color_print import ColorPrint

def ask_shodan(ip):
  print("Asking Shodan.io for additional information...")

  try:
    from wepwawet.API import SHODAN_KEY
  except:
    ColorPrint.red("Unable to import API keys - make sure API.py exists!")
    return

  api = shodan.Shodan(SHODAN_KEY)
  try:
    res = api.host(ip)
    return res
  except Exception as e:
    ColorPrint.red(f"Error while retreiving shodan informations: {e}")