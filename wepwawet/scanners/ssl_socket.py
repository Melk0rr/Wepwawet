import socket
import ssl

from wepwawet.scanners.port import Port
from wepwawet.scanners.url import URL
from wepwawet.scanners.certificate import certificate
from wepwawet.utils.color_print import ColorPrint

# Exemple Usage

# MyURL = SSLSocket(url="https://www.ramsaysante.fr",port=443)
# print(MyURL.URL.get_domain())
# print("TLS 1.0 = ",MyURL.is_tls_enabled(ssl.PROTOCOL_TLSv1))
# print("TLS 1.1 = ",MyURL.is_tls_enabled(ssl.PROTOCOL_TLSv1_1))
# print("TLS 1.2 = ",MyURL.is_tls_enabled(ssl.PROTOCOL_TLSv1_2))

# MyURL.Open_Socket()
# MyURL.Wrap_Socket()
# print(MyURL.get_ssl_version())
# MyURL.close_socket()

# Exemple Usage 2
# MyURL = SSLSocket(url="https://www.ramsaysante.fr",port=443)
# print(MyURL.get_tls_state())
# --> {'result_list': 'False, False, true, true'}

ssl_equiv = (
    ("TLS1.0", ssl.PROTOCOL_TLSv1),
    ("TLS1.1", ssl.PROTOCOL_TLSv1_1),
    ("TLS1.2", ssl.PROTOCOL_TLSv1_2),
    ("TLS1.3", None))


class MySocket:

  URL = None
  socket = None
  is_opened = False
  TLS_PORT_OPENED = False

  def __init__(self, url):
    """ Constructor """
    self.set_url(url)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    self.TLS_PORT_OPENED = self.URL.is_port_in_list(443) or self.check_port()

  def get_url(self):
    """ Getter for the URL """
    return self.URL

  def get_socket(self):
    """ Getter for the socket """
    if self.is_opened:
      return self.socket

  def set_url(self, url):
    """ Setter for the URL """
    if isinstance(url, URL):
      self.URL = url

    else:
      raise ValueError("Provided url must be an instance of the URL class !")

  def check_port(self, port=443):
    """ Check whether or not the given port is open on the URL """
    check = self.socket.connect_ex((self.URL.get_ip(), port))
    if check == 0:
      self.URL.append_open_port(Port(port_number=port))

    return check == 0

  def open_socket(self):
    """ Open the socket """
    
    if not self.TLS_PORT_OPENED:
      print("Port 443 is not opened")
      return -1

    try:
      if self.is_opened:
        print(__class__.__name__ + ": Socket already opened")
        return -1

      else:
        self.socket = socket.create_connection((self.URL.get_domain(), 443))
        self.is_opened = True
        return self.socket

    except:
      self.is_opened = False
      print(__class__.__name__ + ": Error while creating socket")
      return -1

  def close_socket(self):
    """ Close the socket """
    if self.is_opened:
      self.socket.close()

    else:
      print(f"In {__class__.__name__} : Trying to close an unexisting socket")

    self.is_opened = False


class SSLSocket(MySocket):
 
  ssl_context = None
  wrapped_socket = None
  ssl_certificate = None


  def __init__(self, url):
        
    super().__init__(url)
    self.ssl_certificate = certificate()
    #certificate.__init__()

  def get_ssl_context(self):
    """ Getter for SSL context """
    if(self.ssl_context is not None):
      return self.ssl_context

  def get_ssl_version(self):
    """ Returns the SSL version used for the url certificate """
    if self.ssl_certificate.state:
      return self.wrapped_socket.version()

    print(f"In {__class__.__name__} : Socket was not Wrapped")

  def get_ssl_used_cypher(self):
    """ Returns the list of used cyphers """
    if self.ssl_certificate.state:
          return self.wrapped_socket.cipher()
    else:
      ColorPrint.red(f"In {__class__.__name__} :no cypher can be retrieved")

  def get_certificate(self):
    """ Returns the url certificate """
    if self.ssl_certificate.state:
      return self.wrapped_socket.getpeercert()
    else:
      ColorPrint.red(f"In {__class__.__name__} : No certificate can be retrieved")
  
    
  def get_header(self):
    if self.ssl_certificate.state:
      str_Data = f"HEAD / HTTP/1.0\r\nHost: {self.URL.get_domain()}\r\n\r\n"
      str_Encoded = str.encode(str_Data)
      self.wrapped_socket.sendall(str_Encoded)
      return self.wrapped_socket.recv(1024).split(b"\r\n")
    ColorPrint.red(f"In {__class__.__name__} : ERROR Socket is Not Wrapped: No header can be retrieved")
    return {"Targer not wrapped"}

  def wrap_ssl_socket(self, tls_version=None):
    """ Wrap the socket """
    if self.ssl_certificate.state:
      print(f"In {__class__.__name__} : Warning trying to wrap a socket already Wrapped")
      return False

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
        self.ssl_certificate.state = False
        #if err is ssl.ALERT_DESCRIPTION_CERTIFICATE_EXPIRED:
        self.ssl_certificate.reason = err.reason
        self.ssl_certificate.code = err.verify_code
        self.ssl_certificate.message = err.verify_message
     

        ColorPrint.yellow(f"In {__class__.__name__} : Certificate error {err.reason} : {err.verify_code} : {err.verify_message}")

      except Exception as err:
        ColorPrint.yellow(f"In {__class__.__name__} : cannot wrap socket with version {tls_version}: {err}")

      return self.ssl_certificate.state

  # *******************************************************
  # def is_tls_enabled(self,tls_version)
  #   where tls_version can be:
  #       ssl.PROTOCOL_TLSv1
  #       ssl.PROTOCOL_TLSv1_1
  #       ssl.PROTOCOL_TLSv1_2
  #       none for maximum value available (test for TLS1.3)
  # *******************************************************

  def is_tls_enabled(self, tls_version):
    """ Checks if TLS protocol is enabled """
    value = ""
    super().open_socket()

    if self.wrap_ssl_socket(tls_version):
      value = self.get_ssl_version()

    super().close_socket()

    return value

  def get_tls_state(self):
    """ Check every specified TLS version state """
    res = {}

    # Check each version
    for version in ssl_equiv:
      version_name, version_protocol = version
      response = self.is_tls_enabled(version_protocol)
      value = False

      if response:
        if not (version_name == "TLSv1.3" and response != "TLSv1.3"):
          value = True

      res[version_name] = value

    return res
