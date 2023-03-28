""" Target module handling targeting operations and data gathering """
import csv
from time import sleep

from wepwawet.scanners.http import http_info
from wepwawet.scanners.shodan import ask_shodan
from wepwawet.scanners.url import URL
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

    # Clean up targets and init instances
    for i in range(len(self.options["TARGET"])):
      url = URL(self.options["TARGET"][i])
      url.resolve_ip()

      self.options["TARGET"][i] = url

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
      # If option is provided: check for informations with shodan API
      if self.options["--shodan"]:
        try:
          from wepwawet.API import SHODAN_KEY

        except Exception as err:
          self.handle_exception(
              err, "Unable to import API key - make sure API.py exists!")
          return

        shodan_res = ask_shodan(self, target, SHODAN_KEY)

        # Sleep 1s to reduce shodan API calls
        if target.get_ip():
          sleep(1)

      # If option is provided: do a simple http request to the target to retreive status and title
      if self.options["--http-info"]:
        print("\nGathering additional information from http requests...")
        http_res = http_info(self, target)

      final_res = {
          **target.to_dictionary(),
          **shodan_res,
          **http_res
      }

      self.results.append(final_res)

    # Export results to CSV if option is provided
    if self.options["--export-csv"]:
      self.res_2_csv()
