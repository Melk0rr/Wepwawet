from typing import Dict

from wepwawet.network import SSLSocket, Header
from wepwawet.utils import ColorPrint


def check_header(target: "URL") -> Dict:
  """ Main Header function : Retrieve Header """
  response = {
    "Cert State":  "",
    "Cert code": "",
    "Cert reason": "",
    "Cert message": "",
    "Cert validity": "",
    "Cert CN": "",
    "Cert O": "",
    "Certificate": "",
    "Header": ""
  }

  if target.get_ip():
    print(f"{target.get_domain()}: checking header with best SSL connection available", end="...")

    local_ssl_socket = SSLSocket(url=target)
    local_ssl_socket.open_socket()

    try:
      if local_ssl_socket.wrap_ssl_socket(tls_version=None):
        local_ssl_socket.get_header()
        if local_ssl_socket.ssl_certificate.state:
          local_ssl_socket.get_certificate()

        # Analyse header
        try:
          local_ssl_socket.header.analyse()
          local_ssl_socket.header.print_result()

        except Exception as e:
          ColorPrint.red(f"{target.get_domain()}: error while analysing header {e}")

        # Analyse certificate
        try:
          local_ssl_socket.ssl_certificate.analyse()

        except Exception as e:
          ColorPrint.red(f"{target.get_domain()}: error while analysing certificate {e}")
        
    except Exception as e:
      ColorPrint.red(
          f"{target.get_domain()}: error while retrieving Header informations {e}")
  
    response = {
        "Cert State":  local_ssl_socket.ssl_certificate.state,
        "Cert code": local_ssl_socket.ssl_certificate.code,
        "Cert reason": local_ssl_socket.ssl_certificate.reason,
        "Cert message": local_ssl_socket.ssl_certificate.message,
        "Cert validity": local_ssl_socket.ssl_certificate.validity,
        "Cert CN": local_ssl_socket.ssl_certificate.issued_for_cn,
        "Cert O": local_ssl_socket.ssl_certificate.issued_for_o,
        "Certificate": local_ssl_socket.ssl_certificate.data,      
        "Header": local_ssl_socket.header.data
    }
    # add header CSP values 

    local_ssl_socket.close_socket()

  else:
    print(f"{target.get_domain()}: IP not resolved. Skipping...")

  # add header CSP value
  response.update(Header.security_dict.items())
  
  return response
