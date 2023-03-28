""" Target module handling targeting operations and data gathering """
import csv
import re
import socket
from time import sleep
from urllib.parse import urlsplit

from wepwawet.scanners.http import http_info
from wepwawet.scanners.shodan import ask_shodan
from wepwawet.utils.color_print import ColorPrint
from wepwawet.utils.init_option_handle import str_file_option_handle

from .base import Base


class Target(Base):
  """Main enumeration module"""

  results = []

  def handle_exception(self, e, message=""):
    """ Function handling exception for the current class """
    if self.options["--verbose"]:
      print(e)
    if message:
      ColorPrint.red(message)

  def init(self):
    """ Initialization function """
    str_file_option_handle(self, "TARGET", "FILE")

    # Clean up targets
    for i in range(len(self.options["TARGET"])):
      url = self.options["TARGET"][i]

      # Inject protocol if not there
      if not re.match(r'http(s?):', url):
        url = 'http://' + url

      parsed = urlsplit(url)
      host = parsed.netloc
      target_ip = ""

      # Check if target is reachable
      try:
        target_ip = socket.gethostbyname(host)

      except Exception as err:
        self.handle_exception(err,
                              f"Error connecting to {host}! Make sure it is a resolvable address")

      ColorPrint.green(f"Gathering data for {host}")
      self.options["TARGET"][i] = {'host': host, 'ip': target_ip}

  def res_2_csv(self):
    """ Write the results into a CSV file """
    print("\nExporting results to csv...")
    with open(self.options["--export-csv"], "w", encoding="utf-8", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
      writer.writeheader()
      writer.writerows(self.results)

  def run(self):
    # Retreive IP of target and run initial configuration
    self.init()

    for target in self.options["TARGET"]:
      print(f"\n{target['host']}:{target['ip']}")

      # If option is provided: check for informations with shodan API
      if self.options["--shodan"]:
        try:
          from wepwawet.API import SHODAN_KEY
        except Exception as err:
          self.handle_exception(
              err, "Unable to import API key - make sure API.py exists!")
          return

        target = {**target, **ask_shodan(self, target, SHODAN_KEY)}

        # Sleep 1s to reduce shodan API calls
        if target["ip"]:
          sleep(1)

      # If option is provided: do a simple http request to the target to retreive status and title
      if self.options["--http-info"]:
        print("\nGathering additional information from http requests...")
        target = {**target, **http_info(self, target)}

      # If option is provided: do a simple http request to the target to retreive status and title
      if self.options["--check-tls"]:
        print("\nGathering additional information from https TLS acceptance...")
        target = {**target, **check_TLS(self, target)}


      self.results.append(target)

    # Export results to CSV if option is provided
    if self.options["--export-csv"]:
      self.res_2_csv()
