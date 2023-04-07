import ssl
import json
from wepwawet.scanners.ssl_socket import SSLSocket
from wepwawet.scanners.certificate import certificate


def check_header(self, target):
  """ Main Header function : Retrieve Header """
  print(f"Cheking Header for {target.get_domain()}")
  local_ssl_socket = SSLSocket(url=target)
  local_ssl_socket.open_socket()

  response_header = "No header can be retrieved"
  response_state = False
  response_certificate = "No certificate found"

  try:
    state = local_ssl_socket.wrap_ssl_socket(tls_version=None)
    if state:
      response_header = local_ssl_socket.get_header()
      response_certificate = local_ssl_socket.get_certificate() 

  except Exception as e:

    self.handle_exception(
        e, f"Error while retrieving Header informations for {target.get_domain()}")

  response = { 
      "Header": response_header, 
      "Certificate State": local_ssl_socket.ssl_certificate.state,
      "Certificate code": local_ssl_socket.ssl_certificate.code,
      "Certificate reason": local_ssl_socket.ssl_certificate.reason,
      "Certificate message": local_ssl_socket.ssl_certificate.message,
      "Certificate": response_certificate
    }
  local_ssl_socket.close_socket()
  return response