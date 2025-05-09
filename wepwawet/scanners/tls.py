# INFO: Module to check TLS status on URL

from typing import TYPE_CHECKING, Dict

from wepwawet.network.ssl_socket import SSLSocket
from wepwawet.utils.color_print import ColorPrint

if TYPE_CHECKING:
    from wepwawet.network.url import URL


def check_tls(target: "URL") -> Dict:
    """Main TLS function : Check TLS"""

    tls_response = {"TLS1.0": "", "TLS1.1": "", "TLS1.2": "", "TLS1.3": ""}

    if target.get_ip():
        print(f"Cheking TLS for {target.get_domain()}")

        local_ssl_socket = SSLSocket(url=target)

        try:
            tls_response = local_ssl_socket.get_tls_state()

        except Exception as e:
            ColorPrint.red(f"check_tls::Error while checking TLS informations for {target.get_domain()}\n{e}")

    else:
        print(f"{target.get_domain()}: IP not resolved. Skipping...")

    return tls_response
