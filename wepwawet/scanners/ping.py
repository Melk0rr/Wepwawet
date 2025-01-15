""" Simple module to ping a host """
from subprocess import Popen, PIPE, STDOUT

from wepwawet.utils.color_print import ColorPrint

out_function = {
  0: ColorPrint.green,
  1: ColorPrint.red
}

def ping(self, target):
  """ Run ping command on the provided host """
  response = 1

  host_ip = target.get_ip_str()

  if host_ip:
    print(f"{target.get_domain()}, pinging", end="...")

    ping = Popen("ping -w 100 " + host_ip, stderr=STDOUT, stdout=PIPE)
    ping.communicate()

    response = ping.returncode

    msg_variation = "responds" if response == 0 else "does not respond"
    out_function[response](f"{host_ip} {msg_variation} to ping")
  
  else:
    ColorPrint.red(f"{target.get_domain()}, no IP to ping")
    
  return response == 0