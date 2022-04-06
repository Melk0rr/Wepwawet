import os
import re
import socket
import sys
from urllib.parse import urlsplit

from wepwawet.scanners.shodan import ask_shodan
from wepwawet.utils.color_print import ColorPrint
from .base import Base

"""Main enumeration module"""
class Target(Base):

  urls = list()

  def handle_exception(self, e, message=""):
    if self.options["--verbose"]: print(e)
    if message: ColorPrint.red(message)


  def init(self):

    # If user set file option: define target with file content
    if self.options["FILE"]:
      full_path = os.path.join(os.getcwd(), self.options["FILE"])

      with open(full_path) as file:
        self.options["TARGET"] = list(filter(None, file.read().split('\n')))

    # Else: the target is defined by the target option
    else: self.options["TARGET"] = list(filter(None, self.options["TARGET"].split(",")))

    # Clean up targets
    for i in range(len(self.options["TARGET"])):
      url = self.options["TARGET"][i]
      # Inject protocol if not there
      if not re.match(r'http(s?):', url):
        url = 'http://' + url

      parsed = urlsplit(url)
      host = parsed.netloc

      self.options["TARGET"][i] = host

      try:
        ip_str = socket.gethostbyname(host)
        ColorPrint.green(f"Searching for subdomains for {ip_str} ({host})")
      except Exception as e:
        self.handle_exception(e,
                              "Error connecting to target! Make sure you spelled it correctly and it is a resolvable address")
