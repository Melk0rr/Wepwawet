import socket
import shodan

from utils.color_print import ColorPrint

def ask_shodan(self):
  print("Asking Shodan.io for additional information...")

  try:
    from wepwawet.API import SHODAN_KEY
  except:
    ColorPrint.red("Unable to import API key - make sure API.py exists!")
    return

  api = shodan.Shodan(SHODAN_KEY)
  for i in range(len(self.options["TARGET"])):
    try:
      res = api.host(socket.gethostbyname(self.options["TARGET"][i]))
      self.urls.append({
        ""
      })
    except Exception as e:
      self.handle_exception(e, "Error while retreiving shodan informations")