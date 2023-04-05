import ssl
from wepwawet.scanners.ssl_socket import SSLSocket


def check_header(self, target):
  """ Main Header function : Retrieve Header """
  print(f"Cheking Header for {target.get_domain()}")
  
  my_ssl_socket = SSLSocket(url=target)
  response = {"Header": "No header can be retrieved"}
  my_ssl_socket.open_socket()
  try:
    state = my_ssl_socket.wrap_ssl_socket(tls_version=None)
    if state:
      response = { 
        "Header": my_ssl_socket.get_header(),                    
        "Certificate": my_ssl_socket.get_certificate() 
      }
      print(response) 

  except Exception as e:
    self.handle_exception(
        e, f"Error while retrieving Header informations for {target.get_domain()}")

  my_ssl_socket.close_socket()

  return response