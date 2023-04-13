import ssl
from wepwawet.scanners.ssl_socket import SSLSocket
from wepwawet.scanners.certificate import Certificate
from wepwawet.utils.color_print import ColorPrint

def check_header(self, target):
  """ Main Header function : Retrieve Header """
  print(f"Cheking Header for {target.get_domain()} with best SSL connection available")
  local_ssl_socket = SSLSocket(url=target)
  
  local_ssl_socket.open_socket()

  response_header = {"No header can be retrieved"}
  
  try:
    if local_ssl_socket.wrap_ssl_socket(tls_version=None):
      response_header = local_ssl_socket.get_header()
      if local_ssl_socket.ssl_certificate.state:
        local_ssl_socket.ssl_certificate.data = local_ssl_socket.get_certificate()

  except Exception as e:
    ColorPrint.red(f"{e} : Error while retrieving Header informations for {target.get_domain()}")
  
  response = { 
      "Header": response_header, 
      "Cert State":  local_ssl_socket.ssl_certificate.state,
      "Cert code": local_ssl_socket.ssl_certificate.code,
      "Cert reason": local_ssl_socket.ssl_certificate.reason,
      "Cert message": local_ssl_socket.ssl_certificate.message,
      "Cert self signed": local_ssl_socket.ssl_certificate.self_signed,
      "Cert still valid ": local_ssl_socket.ssl_certificate.still_valid,
      
      "Certificate ": local_ssl_socket.ssl_certificate.data
    }
  
  local_ssl_socket.ssl_certificate.Analyse()

  local_ssl_socket.close_socket()

  return response