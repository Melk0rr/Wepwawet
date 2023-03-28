""" URL module adressing url object behaviour """
import re
import socket
from urllib.parse import urlsplit, urlparse

from wepwawet.utils.color_print import ColorPrint
from wepwawet.scanners.port import Port


class URL:
  """ URL class implementation """

  host = ""
  domain = ""
  ip = ""
  open_ports = []
  related_domains = []
  geo_location = {
      "city": None,
      "country": None
  }

  def __init__(self, url):
    """ Constructor """
    # Inject protocol if not there
    if not re.match(r'http(s?):', url):
      url = 'http://' + url

    self.set_url(url)

  def get_host(self):
    """ Getter for the URL """
    return self.host

  def get_ip(self):
    """ Getter for the IP """
    return self.ip

  def get_domain(self):
    """ Getter for the Domain """
    return self.domain

  def get_port_numbers(self):
    """ Getter for the Port numbers """
    return [p.get_number() for p in self.open_ports]

  def get_port_strings(self):
    """ Getter for the Port strings """
    return [p.to_string() for p in self.open_ports]

  def get_geo_str(self):
    """ Returns a string based on the geolocation infos """
    return f"{self.geo_location['city']}, {self.geo_location['country']}"

  def set_url(self, url):
    """ Set the URL and the domain """
    if self.is_valid_url(url):
      self.host = url
      self.domain = self.extract_domain()

    else:
      raise Exception(f"Invalid URL provided: {url} !")

  def set_open_ports(self, ports):
    """ Set the open ports """
    for p in ports:
      self.append_open_port(p)

  def set_related_domains(self, domains):
    """ Set the host related domains """
    self.related_domains = domains

  def set_geo_location(self, city, country):
    """ Set the geo location infos """
    self.geo_location = {
        "city": city,
        "country": country
    }

    print(f"{self.domain} is hosted in {self.get_geo_str()}")

  def append_open_port(self, port):
    """ Append the port to the list of open ports """
    if isinstance(port, Port):
      self.open_ports.append(port)

    else:
      raise ValueError("Provided port must be an instance of class Port")

  def extract_domain(self):
    """ Extract domain from url """
    return urlsplit(self.host).netloc

  def is_valid_url(self, url):
    """ Checks whether the given URL is valid """
    try:
      parsed = urlparse(url)
      return all([parsed.scheme, parsed.netloc])

    except:
      return False

  def resolve_ip(self):
    """ Resolves the IP address for the current URL """
    try:
      ip = socket.gethostbyname(self.domain)
      self.ip = ip
      ColorPrint.green(f"\n{self.domain}: {self.ip}")

    except:
      ColorPrint.red(f"Could not resolve IP address for {self.domain}")

  def geo_locate(self):
    """ Retrieves the geo location informations for the current URL """

  def to_dictionary(self):
    """ Returns a dictionary based on the instance attributes """
    return {
        "host": self.domain,
        "ip": self.ip,
        **self.geo_location,
        "domains": ', '.join(f"{x}" for x in self.related_domains),
        "ports": ', '.join(f"{x}" for x in self.get_port_numbers()),
        "products": ', '.join(f"{x}" for x in self.get_port_strings())
    }
