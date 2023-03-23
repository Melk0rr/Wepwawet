import socket
import ssl


def get_tls_version(url):
  """ Returns the tls version used by the given url """
  context = ssl.create_default_context()
  crt_version = None
  crt_valid = True
  
  try:
    with socket.create_connection((url, 443)) as sock:
      with context.wrap_socket(sock, server_hostname=url) as ssock:
        crt_version = ssock.version()
  
  except ssl.SSLCertVerificationError:
    crt_valid = False
    crt_version = "Invalid"

  return { "crt_valid": crt_valid, "crt_version": crt_version }
