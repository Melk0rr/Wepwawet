""" Target module handling targeting operations and data gathering """
import csv
from time import sleep

from wepwawet.scanners.http import http_info
from wepwawet.scanners.shodan import ask_shodan
from wepwawet.scanners.url import URL
from wepwawet.scanners.geoloc import geoloc
from wepwawet.scanners.tls import check_tls
from wepwawet.utils.color_print import ColorPrint
from wepwawet.utils.init_option_handle import str_file_option_handle

from .base import Base


class Target(Base):
  """Main enumeration module"""

  results = []

  def __init__(self, options):
    """ Constructor """
    super().__init__(options)

    str_file_option_handle(self, "TARGET", "FILE")

    # Clean up targets and init instances
    for i in range(len(self.options["TARGET"])):
      url = URL(self.options["TARGET"][i])
      url.resolve_ip()

      self.options["TARGET"][i] = url

  def handle_exception(self, e, message=""):
    """ Function handling exception for the current class """
    if self.options["--verbose"]:
      print(e)
    if message:
      ColorPrint.red(message)

  def res_2_csv(self):
    """ Write the results into a CSV file """
    print("\nExporting results to csv...")

    with open(self.options["--export-csv"], "w", encoding="utf-8", newline="") as f:
      writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
      writer.writeheader()
      writer.writerows(self.results)

  def run(self):
    # Retreive IP of target and run initial configuration
    for target in self.options["TARGET"]:
      options_res = {}

      # If option is provided: check for informations with shodan API
      if self.options["--shodan"]:
        try:
          from wepwawet.API import SHODAN_KEY

        except Exception as err:
          self.handle_exception(
              err, "Unable to import API key - make sure API.py exists!")
          return

        options_res.update(ask_shodan(self, target, SHODAN_KEY))

        # Sleep 1s to reduce shodan API calls
        if target.get_ip():
          sleep(1)

      # If option is provided: do a simple http request to the target to retreive status and title
      if self.options["--http-info"]:
        print("\nGathering additional information from http requests...")
        options_res.update(http_info(self, target))

      # If option is provided: geo locate the target
      if self.options["--geo-locate"]:
        print(f"\nGeo locating the target...")
        geoloc(self, target)

      # If option is provided: do a simple check to the target to retreive TLS status
      if self.options["--check-tls"]:
        print("\nGathering additional information from https TLS acceptance...")
        options_res.update(check_tls(self, target))

      final_res = {
          **target.to_dictionary(),
          **options_res
      }

      self.results.append(final_res)

    # Export results to CSV if option is provided
    if self.options["--export-csv"]:
      self.res_2_csv()
