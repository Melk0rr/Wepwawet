from wepwawet.network.ssl_socket import SSLSocket
from wepwawet.utils.color_print import ColorPrint


def check_tls(target):
  """ Main TLS function : Check TLS """
  tls_response = {}

  if target.get_ip():
    print(f"Cheking TLS for {target.get_domain()}")

    local_ssl_socket = SSLSocket(url=target)

    try:
      tls_response = local_ssl_socket.get_tls_state()

    except Exception as e:
      ColorPrint.red(
          f"{e} : Error while checking TLS informations for {target.get_domain()}")

  else:
    print(f"{target.get_domain()}: IP not resolved. Skipping...")

  return tls_response
