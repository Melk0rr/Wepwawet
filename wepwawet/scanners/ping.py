""" Simple module to ping a host """
import os

from wepwawet.utils.color_print import ColorPrint


def ping(target):
  """ Run ping command on the provided host """
  host_ip = target.get_ip()
  response = 1

  if host_ip:
    response = os.system("ping -w 100 " + host_ip)

    if response == 0:
      ColorPrint.green(f"{host_ip} responds to ping command")
    
    else:
      ColorPrint.red(f"{host_ip} does not respond to ping command")
  
  else:
    ColorPrint.red(f"No IP to ping for {target.get_host()}. Ping aborted")

  return response == 0