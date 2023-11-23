""" Target module handling targeting operations and data gathering """
import csv
from time import sleep
from multiprocessing import Pool

from wepwawet.scanners.geoloc import geoloc
from wepwawet.scanners.header import check_header
from wepwawet.scanners.http import http_info
from wepwawet.scanners.ping import ping
from wepwawet.scanners.shodan import ask_shodan
from wepwawet.scanners.tls import check_tls
from wepwawet.network.url import URL
from wepwawet.scanners.nmap import nmap
from wepwawet.scanners.whois import whois
from wepwawet.utils.color_print import ColorPrint
from wepwawet.utils.init_option_handle import str_file_option_handle

from .base import Base


class Target(Base):
  """Main enumeration module"""
  
  def __init__(self, options):
    """ Constructor """
    super().__init__(options)

    self.results = []
    self.unique_targets = []

    str_file_option_handle(self, "TARGET", "FILE")
    self.unique_targets = list(set(self.options["TARGET"]))
    print(f"Investigating {len(self.unique_targets)} hosts...")

    # Clean up targets and init instances
    unique_urls = []
    with Pool(processes=5) as pool:
      for url in pool.imap_unordered(self.init_url, self.unique_targets):
        unique_urls.append(url)

    self.unique_targets = unique_urls

  def init_url(self, target):
    """ Init url instance based on target index and resolve ip address """
    url = URL(target)
    url.resolve_ip()

    return url

  def handle_exception(self, e, message=""):
    """ Function handling exception for the current class """
    if self.options["--verbose"]:
      print(e)
      
    if message:
      ColorPrint.red(message)

  def res_2_csv(self):
    """ Write the results into a CSV file """
    print("\nExporting results to csv...")

    if len(self.results) <= 0:
      ColorPrint.red(f"Error while exporting results to CSV: ({len(self.results)} results)s")
      return 0

    try:
      with open(self.options["--export-csv"], "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
        writer.writeheader()
        writer.writerows(self.results)

    except Exception as e:
      ColorPrint.red(f"{__class__.__name__} : {e} cannot save to CSV")

  def url_process(self, target):
    """ Target process to deal with url data """
    options_res = {}

    # If option is provided run ping on the target
    if self.options["--ping"]:
      respond = ping(target)
      options_res.update({ "ping": "YES" if respond else "NO" })

    # If option is provided: check for informations with shodan API
    if self.options["--shodan"]:
      options_res.update(ask_shodan(self, target))

    # If option is provided: do a simple http request to the target to retreive status and title
    if self.options["--http-info"]:
      print("\nGathering additional information from http requests...")
      options_res.update(http_info(self, target))

    # If option is provided: geo locate the target
    if self.options["--geo-locate"]:
      print(f"\nGeo locating the target...")
      geoloc(self, target)

    # If option is provided: scan target with nmap
    if self.options["--nmap"]:
      nmap(self, target)

    # If option is provided: do a simple check to the target to retreive TLS status
    if self.options["--check-tls"]:
      print("\nGathering additional information from https TLS acceptance...")
      options_res.update(check_header(target))
      options_res.update(check_tls(target))

    if self.options["--whois"]:
      print("\nChecking Who.is...")
      whois(self, target)

    return {
      **target.to_dictionary(),
      **options_res
    }


  def run(self):
    # Retreive IP of target and run initial configuration
    with Pool(processes=5) as pool:
      for url_data in pool.imap_unordered(self.url_process, self.unique_targets):
        self.results.append(url_data)

    # Export results to CSV if option is provided
    if self.options["--export-csv"]:
      self.res_2_csv()
