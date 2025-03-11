# INFO: Simple module to ping a host

from subprocess import PIPE, STDOUT, Popen
from typing import TYPE_CHECKING

from wepwawet.utils import ColorPrint

out_function = {0: ColorPrint.green, 1: ColorPrint.red}

if TYPE_CHECKING:
    from wepwawet.network.url import URL


def ping(self, target: "URL") -> bool:
    """Run ping command on the provided host"""
    response = 1

    host_ip = str(target.get_ip())

    if host_ip:
        print(f"{target.get_domain()}, pinging", end="...")

        ping = Popen(["ping", "-w", "100", host_ip], stderr=STDOUT, stdout=PIPE)
        ping.communicate()

        response = ping.returncode

        msg_variation = "responds" if response == 0 else "does not respond"
        out_function[response](f"{host_ip} {msg_variation} to ping")

    else:
        ColorPrint.red(f"{target.get_domain()}, no IP to ping")

    return response == 0
