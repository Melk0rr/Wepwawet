""" Target module handling targeting operations and data gathering """
import os
import re
import csv
import socket
from urllib.parse import urlsplit

from wepwawet.utils.color_print import ColorPrint
from wepwawet.utils.dictionary_join import join_dictionary_values
from wepwawet.scanners.shodan import ask_shodan
from wepwawet.scanners.http import http_info

from .base import Base


class Target(Base):
  """Main enumeration module"""

  urls = []

  def handle_exception(self, e, message=""):
    """ Function handling exception for the current class """
    if self.options["--verbose"]:
      print(e)
    if message:
      ColorPrint.red(message)


  def init(self):
    """ Initialization function """
    # If user set file option: define target with file content
    if self.options["FILE"]:
      full_path = os.path.join(os.getcwd(), self.options["FILE"])

      with open(full_path, encoding="utf-8") as file:
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
      except Exception as err:
        self.handle_exception(err,
        f"Error connecting to {host}! Make sure you spelled it correctly and it is a resolvable address")

      self.options["TARGET"][i] = { 'host': host, 'ip': target_ip }


  def res_2_csv(self):
    """ Write the results into a CSV file """
    print("\nExporting results to csv...")
    with open(self.options["--export-csv"], "w", encoding="utf-8", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=self.urls[0].keys())
      writer.writeheader()
      writer.writerows(self.urls)


  def run(self):
    # Retreive IP of target and run initial configuration
    self.init()

    ask_shodan(self)

    if self.options["--http-info"]:
      print("\nGathering additional information from http requests...")
      for i in range(len(self.options["TARGET"])):
        http_info(self, self.options["TARGET"][i])

    if self.options["--export-csv"]:
      self.res_2_csv()
    