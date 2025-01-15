""" URL module adressing url object behaviour """
import re
import socket

from typing import List, Dict
from urllib.parse import urlparse, urlsplit

from wepwawet.network.ipv4 import IPv4
from wepwawet.utils import ColorPrint


class URL:
  """ URL class implementation """

  def __init__(self, url: str):
    """ Constructor """
    # Inject protocol if not there
    if not re.match(r'http(s?):', url):
      url = 'http://' + url

    if not self.is_valid_url(url):
      raise ValueError(f"Invalid URL provided: {url} !")

    self.host = url
    self.netloc = urlsplit(self.host).netloc
    self.ip: IPv4 = None
    self.related_domains: List[str] = []
    self.geo_location = {
        "city": "",
        "country": ""
    }

  def get_host(self) -> str:
    """ Getter for the URL """
    return self.host

  def get_ip(self) -> IPv4:
    """ Getter for the IP """
    return self.ip

  def get_domain(self) -> str:
    """ Getter for the Domain """
    return self.netloc

  def get_geo_str(self) -> str:
    """ Returns a string based on the geolocation infos """
    city = self.geo_location['city']
    country = self.geo_location['country']
    separator = ", " if city and country else ""
    return f"{city}{separator}{country}"

  def get_ip_str(self) -> str:
    """ Returns current ip address string """
    if self.ip:
      return str(self.ip)

  def set_ip(self, ip: IPv4):
    """ Setter for url ip address """
    self.ip = ip

  def set_related_domains(self, domains: List[str]):
    """ Set the host related domains """
    self.related_domains = domains

  def set_geo_location(self, country: str, city: str):
    """ Set the geo location infos """

    if (city is None) or (len(city) <= 0):
      city = self.geo_location['city']

    if (country is None) or (len(country) <= 0):
      country = self.geo_location['country']

    self.geo_location = {
        "city": city,
        "country": country
    }

    print(f"{self.netloc} is hosted in {self.get_geo_str()}")

  def is_valid_url(self, url: str) -> bool:
    """ Checks whether the given URL is valid """
    try:
      parsed = urlparse(url)
      return all([parsed.scheme, parsed.netloc])

    except:
      return False

  def resolve_ip(self, ip_track: Dict = {}):
    """ Resolves the IP address for the current URL """
    try:
      ip = socket.gethostbyname(self.netloc)
      
      if ip:
        self.ip = IPv4(ip)

      ColorPrint.green(f"{self.netloc}: {self.ip}")

    except Exception as e:
      ColorPrint.red(f"{self.netloc}: could not resolve IP address > {e}")

  def to_dictionary(self) -> Dict:
    """ Returns a dictionary based on the instance attributes """

    formated_ports = ', '.join(f"{x}" for x in self.ip.get_port_numbers()) if self.ip else ""
    formated_ports_str = ', '.join(f"{x}" for x in self.ip.get_port_strings()) if self.ip else ""
    return {
        "host": self.netloc,
        "ip": self.get_ip_str(),
        **self.geo_location,
        "domains": ', '.join(f"{x}" for x in self.related_domains),
        "ports": formated_ports,
        "products": formated_ports_str
    }
