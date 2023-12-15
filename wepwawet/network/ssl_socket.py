import socket
import ssl

from wepwawet.network.port import Port
from wepwawet.network.url import URL
from wepwawet.network.certificate import Certificate
from wepwawet.utils.color_print import ColorPrint

# Exemple Usage

# MyURL = SSLSocket(url="https://www.google.fr",port=443)
# print(MyURL.URL.get_domain())
# print("TLS 1.0 = ",MyURL.is_tls_enabled(ssl.PROTOCOL_TLSv1))
# print("TLS 1.1 = ",MyURL.is_tls_enabled(ssl.PROTOCOL_TLSv1_1))
# print("TLS 1.2 = ",MyURL.is_tls_enabled(ssl.PROTOCOL_TLSv1_2))

# MyURL.Open_Socket()
# MyURL.Wrap_Socket()
# print(MyURL.get_ssl_version())
# MyURL.close_socket()

# Exemple Usage 2
# MyURL = SSLSocket(url="https://www.google.fr",port=443)
# print(MyURL.get_tls_state())
# --> {'result_list': 'False, False, true, true'}

ssl_equiv = (
    ("TLS1.0", ssl.PROTOCOL_TLSv1),
    ("TLS1.1", ssl.PROTOCOL_TLSv1_1),
    ("TLS1.2", ssl.PROTOCOL_TLSv1_2),
    ("TLS1.3", None))

index_ssl = ["", "", "", "TLS1.0", "TLS1.1", "TLS1.2","TLS1.3"]


class Header:
  def __init__(self):
    """ Constructor """

    self.state= False
    self.data = "No header"
    self.csp = "[NONE]"
    self.hsts = "[NONE]"
    self.x_content = "[NONE]"
    self.x_frame = "[NONE]"


  def check_header(self,security):
    """ Check if the website implement security best practices into data"""

    if type(self.data) is list:
      for el in self.data:
        if security in el:
          ColorPrint.green(f"Found {security} in {el}")
          return el

    return "[NONE]"    

  
  def analyse(self):
    """ Analyse the header to check for security implementations """
    self.csp = self.check_header(b"Content-Security-Policy")
    self.hsts = self.check_header(b"Strict-Transport-Security")
    self.x_content = self.check_header(b"X-Content-Type-Options")
    self.x_frame = self.check_header(b"X-Frame-Options")
    

class MySocket:

  def __init__(self, url):
    """ Constructor """
    if not isinstance(url, URL):
      raise ValueError("Provided url must be an instance of the URL class !")
    
    self.URL = url
    self.is_opened = False
    self.set_url(url)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.TLS_PORT_OPENED = self.URL.get_ip().is_port_in_list(443) or self.check_port()

  def get_url(self):
    """ Getter for the URL """
    return self.URL

  def get_socket(self):
    """ Getter for the socket """
    if self.is_opened:
      return self.socket

  def set_url(self, url):
    """ Setter for the URL """
    if not isinstance(url, URL):
      raise ValueError("Provided url must be an instance of the URL class !")
      
    self.URL = url
      

  def check_port(self, port=443):
    """ Check whether or not the given port is open on the URL """
    check = self.socket.connect_ex((self.URL.get_ip().get_address(), port))
    if check == 0:
      self.URL.get_ip().append_open_port(Port(port_number=port))

    return check == 0

  def open_socket(self):
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

  def close_socket(self):
    """ Close the socket """
    if self.is_opened:
      self.socket.close()

    self.is_opened = False


class SSLSocket(MySocket):

  def __init__(self, url):
    super().__init__(url)
    self.ssl_context = None
    self.wrapped_socket = None
    self.ssl_certificate = Certificate()
    self.header = Header()

  def get_ssl_context(self):
    """ Getter for SSL context """

    if(self.ssl_context is not None):
      return self.ssl_context

  def get_ssl_version(self):
    """ Returns the SSL version used for the url certificate """
    version = ""
    if self.ssl_certificate.state:
      version = self.wrapped_socket.version()
    
    else:
      ColorPrint.red(f"In {__class__.__name__} :no SSL can be retrieved")

    return version

  def get_ssl_used_cypher(self):
    """ Returns the list of used cyphers """
    if self.ssl_certificate.state:
      return self.wrapped_socket.cipher()
    
    else:
      ColorPrint.red(f"In {__class__.__name__} :no cypher can be retrieved")

  def get_certificate(self):
    """ Returns the url certificate """
    if self.ssl_certificate.state:
      try:
        self.ssl_certificate.data = self.wrapped_socket.getpeercert()

      except Exception as err:
        ColorPrint.red(f"In {__class__.__name__} - {err} :getPeerCert error")

    else:
      ColorPrint.red(
          f"In {__class__.__name__} : No certificate can be retrieved")



  def get_header(self):
    if self.ssl_certificate.state:
      str_Data = f"HEAD / HTTP/1.0\r\nHost: {self.URL.get_domain()}\r\n\r\n"
      str_Encoded = str.encode(str_Data)
      self.wrapped_socket.sendall(str_Encoded)
      self.header.data = self.wrapped_socket.recv(1024).split(b"\r\n")
      self.header.state = True

    else:
       ColorPrint.red(f"In {__class__.__name__} : ERROR Socket is Not Wrapped: No header can be retrieved")
    
    return self.header.state


  def wrap_ssl_socket(self, tls_version=None):
    """ Wrap the socket """
    self.ssl_certificate.state = False
    if self.ssl_certificate.state:
      print(
          f"In {__class__.__name__} : Wrap_ssl_socket is trying to wrap a socket already wrapped")
    else:
      # Setting ssl context based on specified tls version
      try:
        self.ssl_context = ssl.create_default_context()

        if tls_version != None:
          self.ssl_context = ssl.SSLContext(tls_version or ssl.PROTOCOL_SSLv23)

      except Exception as e:
        ColorPrint.red(f"In {__class__.__name__} : {type(err).__name__} {e}")
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

        ColorPrint.yellow(
            f"In {__class__.__name__} : Wrap error {index_ssl[tls_version]}: {err}")

    return self.ssl_certificate.state

  # *******************************************************
  # def is_tls_enabled(self,tls_version)
  #   where tls_version can be:
  #       ssl.PROTOCOL_TLSv1
  #       ssl.PROTOCOL_TLSv1_1
  #       ssl.PROTOCOL_TLSv1_2
  #       none for maximum value available (test for TLS1.3)
  # *******************************************************

  def is_tls_enabled(self, tls_to_test):
    """ Checks if TLS protocol is enabled """
    enabled = False
    
    if self.wrap_ssl_socket(tls_version=tls_to_test):
      ColorPrint.green(f"{self.URL.get_domain()} supports {self.get_ssl_version()}")
      enabled = True

    return enabled

  def get_tls_state(self):
    """Check evry specified TLS version State"""

    res = {}

    # Check each version
    for version in ssl_equiv:
      self.open_socket()
      self.ssl_certificate.state = False

      version_name, version_protocol = version
      value = False

      try:
        response = self.is_tls_enabled(version_protocol)

        if response:
          if not (version_name == "TLSv1.3" and response != "TLSv1.3"):
            value = True

      except Exception as err:
        ColorPrint.yellow(f"{err}: cannot retrieve data for {version}")

      res[version_name] = value
      self.close_socket()

    return res
