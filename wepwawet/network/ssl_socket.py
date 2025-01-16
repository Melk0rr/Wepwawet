import socket
import ssl

from typing import List, Dict, Union, Tuple
from wepwawet.utils import ColorPrint

from .port import Port
from .url import URL
from .certificate import Certificate

ssl_equiv = (
    ("TLS1.0", ssl.PROTOCOL_TLSv1),
    ("TLS1.1", ssl.PROTOCOL_TLSv1_1),
    ("TLS1.2", ssl.PROTOCOL_TLSv1_2))

class Header:

  security_dict = { 'Content-Security-Policy': "[NONE]",
                    'Strict-Transport-Security': "[NONE]",
                    'X-Content-Type-Options': "[NONE]",
                    'X-Frame-Options': "[NONE]"
                   }


  def __init__(self):
    """ Constructor """
    self.state= False
    self.data = "[NONE]"

  def look_for(self, security: str) -> Union[str, List[str]]:
    """ Check if the website implement security best practices into data"""
    search = [ el for el in self.data if security in el ]
    if len(search) > 0:
      return search

    else:
      return "[NONE]"

  def analyse(self) -> None:
    """ Analyse the header to check for security implementations """
    for e in list(self.security_dict.keys()):
      self.security_dict[e]=self.look_for(e)

  def print_result(self) -> None:
    """ Print security search result from header """
    for e in list(self.security_dict.keys()):
      if self.security_dict[e]:
        ColorPrint.green(f"Found {self.security_dict[e]}")

      else:
        ColorPrint.red(f"Not Found {self.security_dict[e]}")


class MySocket:

  def __init__(self, url: URL):
    """ Constructor """
    if not isinstance(url, URL):
      raise ValueError("Provided url must be an instance of the URL class !")
    
    self.is_opened = False

    self.URL = url
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.TLS_PORT_OPENED = False
    if self.URL.get_ip():
      self.TLS_PORT_OPENED = self.URL.get_ip().is_port_in_list(443) or self.check_port()

  def get_url(self) -> URL:
    """ Getter for the URL """
    return self.URL

  def get_socket(self) -> socket.socket:
    """ Getter for the socket """
    if self.is_opened:
      return self.socket

  def set_url(self, url: URL) -> None:
    """ Setter for the URL """
    if not isinstance(url, URL):
      raise ValueError("Provided url must be an instance of the URL class !")
      
    self.URL = url 
      

  def check_port(self, port: int = 443) -> bool:
    """ Check whether or not the given port is open on the URL """
    check = False
    if self.URL.get_ip():
      check = self.socket.connect_ex((self.URL.get_ip_str(), port)) == 0
      if check:
        self.URL.get_ip().append_open_port(Port(port_number=port))

    return check

  def open_socket(self) -> socket.socket:
    """ Open the socket """
    res = -1

    if self.TLS_PORT_OPENED:
      try:
        if self.is_opened:
          print(__class__.__name__ + ": Socket already opened")

        else:
          self.socket = socket.create_connection((self.URL.get_domain(), 443))
          self.is_opened = True
          res = self.socket

      except:
        self.is_opened = False
        ColorPrint.red(__class__.__name__ + ": Error while creating socket")
    
    else:
      print("Port 443 is not opened")

    return res

  def close_socket(self) -> None:
    """ Close the socket """
    if self.is_opened:
      self.socket.close()

    self.is_opened = False


class SSLSocket(MySocket):

  def __init__(self, url: URL):
    super().__init__(url)
    self.ssl_context: ssl.SSLContext = None
    self.wrapped_socket: ssl.SSLSocket = None
    self.ssl_certificate: Certificate = Certificate()
    self.header: Header = Header()

  def get_ssl_context(self) -> ssl.SSLContext:
    """ Getter for SSL context """

    if(self.ssl_context is not None):
      return self.ssl_context

  def get_ssl_version(self) -> str:
    """ Returns the SSL version used for the url certificate """
    version = None
    if self.ssl_certificate.state:
      version = self.wrapped_socket.version()

    else:
      ColorPrint.red(f"In {__class__.__name__} :no SSL can be retrieved")

    return version

  def get_ssl_used_cipher(self) -> Tuple[str, str, int]:
    """ Returns the list of used cyphers """
    cipher = None
    if self.ssl_certificate.state:
      cipher = self.wrapped_socket.cipher()
    
    else:
      ColorPrint.red(f"In {__class__.__name__} :no cypher can be retrieved")
      
    return cipher

  def get_certificate(self) -> None:
    """ Returns the url certificate """
    if self.ssl_certificate.state:
      try:
        self.ssl_certificate.data = self.wrapped_socket.getpeercert()

      except Exception as err:
        ColorPrint.red(f"In {__class__.__name__} - {err} :getPeerCert error")

    else:
      ColorPrint.red(
          f"In {__class__.__name__} : No certificate can be retrieved")

  def get_header(self) -> bool:
    if self.ssl_certificate.state:
      request = f"HEAD / HTTP/1.0\r\nHost: {self.URL.get_domain()}\r\n\r\n"
      self.wrapped_socket.sendall(request.encode())
      str_data = self.wrapped_socket.recv(1024).decode()
      self.header.data= str_data.split("\r\n")
      self.header.state = True

    else:
       ColorPrint.red(f"In {__class__.__name__} : ERROR Socket is Not Wrapped: No header can be retrieved")
    
    return self.header.state


  def wrap_ssl_socket(self, tls_version: str = None) -> bool:
    """ Wrap the socket """
    self.ssl_certificate.state = False
    # Setting ssl context based on specified tls version
    try:
      self.ssl_context = ssl.create_default_context()

      if tls_version != None:
        self.ssl_context = ssl.SSLContext(tls_version or ssl.PROTOCOL_SSLv23)

    except Exception as e:
      ColorPrint.red(f"In {__class__.__name__} : {type(e).__name__} {e}")
      return False

    # Wrapping the socket
    try:
      self.wrapped_socket = self.ssl_context.wrap_socket(
          self.get_socket(), server_hostname=self.URL.get_domain())
      self.ssl_certificate.state = True

    except ssl.SSLCertVerificationError as err:
      self.ssl_certificate.reason = err.reason
      self.ssl_certificate.code = err.verify_code
      self.ssl_certificate.message = err.verify_message

      ColorPrint.yellow(
          f"In {__class__.__name__} : Certificate error {err.reason} : {err.verify_code} : {err.verify_message}")

    except Exception as err:
      self.ssl_certificate.state = False
      ColorPrint.yellow(f"In {__class__.__name__} : Wrap error : {err}")

    return self.ssl_certificate.state


  def get_tls_state(self) -> Dict:
    """Check evry specified TLS version State"""
    res = {
      "TLS1.0" : "",
      "TLS1.1" : "",
      "TLS1.2" : ""
    }

    # Check each version
    for version in ssl_equiv:
      value = False
      if (self.open_socket() != -1):
        version_name, version_protocol = version

        try:
          response = self.wrap_ssl_socket(version_protocol)
          if response:
            ssl_version = self.get_ssl_version()
            value = ((version_name == "TLS1.2" and ssl_version == "TLSv1.2") 
              or (version_name == "TLS1.1" and ssl_version == "TLSv1.1")  
              or (version_name == "TLS1.0" and ssl_version == "TLSv1.0"))
            
            if value:
              ColorPrint.green(f"{self.URL.get_domain()} {version_name} is supported")
            else:
              ColorPrint.red(f"{self.URL.get_domain()} {version_name} is not supported")
          else: 
              ColorPrint.red(f"{self.URL.get_domain()} {version_name} is not supported, serveur does not  reply")

        except Exception as err:
          ColorPrint.yellow(f"{err}:{self.URL.get_domain()} {version_name} is not defined")

        res[version_name] = value
        self.close_socket()

    return res
  