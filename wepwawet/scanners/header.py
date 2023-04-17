from wepwawet.scanners.ssl_socket import SSLSocket
from wepwawet.utils.color_print import ColorPrint



def check_header(target):
  """ Main Header function : Retrieve Header """
  print(
      f"Cheking Header for {target.get_domain()} with best SSL connection available")
  local_ssl_socket = SSLSocket(url=target)
  local_ssl_socket.open_socket()


  try:
    if local_ssl_socket.wrap_ssl_socket(tls_version=None):
      local_ssl_socket.get_header()
      if local_ssl_socket.ssl_certificate.state:
        local_ssl_socket.get_certificate()

      try:
        local_ssl_socket.header.Analyse()
      except Exception as e:
        ColorPrint.red(f"{e} : Error while analysing Header of {target.get_domain()}")

      try:
        local_ssl_socket.ssl_certificate.analyse()
      except Exception as e:
        ColorPrint.red(f"{e} : Error while analysing certificate of {target.get_domain()}")
      

  except Exception as e:
    ColorPrint.red(
        f"{e} : Error while retrieving Header informations for {target.get_domain()}")
 


  response = {
      "Cert State":  local_ssl_socket.ssl_certificate.state,
      "Cert code": local_ssl_socket.ssl_certificate.code,
      "Cert reason": local_ssl_socket.ssl_certificate.reason,
      "Cert message": local_ssl_socket.ssl_certificate.message,
      "Cert validity": local_ssl_socket.ssl_certificate.validity,
      "Certificate": local_ssl_socket.ssl_certificate.data,
      "Header csp": local_ssl_socket.header.csp,
      "Header hsts": local_ssl_socket.header.hsts,
      "Header x-frame": local_ssl_socket.header.x_frame,
      "Header x-content": local_ssl_socket.header.x_content,
      "Header": local_ssl_socket.header.data
  }

  local_ssl_socket.close_socket()
  return response
