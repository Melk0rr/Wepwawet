import os
import re
import socket
import sys
from urllib.parse import urlsplit

from .base import Base
from wepwawet.utils.color_print import ColorPrint
from wepwawet.utils.dictionary_join import join_dictionary_values
from wepwawet.scanners.shodan import ask_shodan
from wepwawet.scanners.http import http_info

'''Main enumeration module'''
class Target(Base):

  urls = list()

  def handle_exception(self, e, message=""):
    if self.options["--verbose"]:
      print(e)
    if message:
      ColorPrint.red(message)


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
      target_ip = ""

      try:
        target_ip = socket.gethostbyname(host)
        ColorPrint.green(f"Gathering data for {target_ip} ({host})")
      except Exception as e:
        self.handle_exception(e, f"Error connecting to {host}! Make sure you spelled it correctly and it is a resolvable address")

      self.options["TARGET"][i] = { 'host': host, 'ip': target_ip }


  def print_urls_result(self):
    ColorPrint.green("|".join([*self.urls[0]]))
    for url in self.urls:
      ColorPrint.green(join_dictionary_values(url, "|"))
  

  def run(self):
    # Retreive IP of target and run initial configuration
    self.init()

    ask_shodan(self)

    if self.options["--http-info"]:
      print("Gathering additional information from http requests...")
      for i in range(len(self.options["TARGET"])):
        http_info(self, self.options["TARGET"][i])

    self.print_urls_result()