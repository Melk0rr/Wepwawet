from wepwawet.scanners.ssl_socket import SSLSocket


def check_tls(self, target):
  """ Main TLS function : Check TLS """
  print(f"Cheking TLS for {target.get_domain()}")

  my_ssl_socket = SSLSocket(url=target)
  tls_response = {}

  try:
    tls_response = my_ssl_socket.get_tls_state()
    print(tls_response)

  except Exception as e:
    self.handle_exception(
        e, f"Error while checking TLS informations for {target.get_domain()}")

  return tls_response
