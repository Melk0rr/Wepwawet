""" Simple module to ping a host """
import os

from wepwawet.utils.color_print import ColorPrint

out_function = {
  0: ColorPrint.green,
  1: ColorPrint.red
}

def ping(self, target):
  """ Run ping command on the provided host """
  response = 1

  host_ip = target.get_ip_address()

  if host_ip:
    response = os.system("ping -w 100 " + host_ip)

    msg_variation = "responds" if response == 0 else "does not respond"
    out_function[response](f"{host_ip} {msg_variation} to ping command")
  
  else:
    ColorPrint.red(f"No IP to ping for {target.get_domain()}. Ping aborted")
    
  return response == 0