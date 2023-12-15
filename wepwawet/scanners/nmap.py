import nmap3

from wepwawet.network.port import Port

nmap = nmap3.Nmap()

nmap_commands = {
  "dns-brute": nmap.nmap_dns_brute_script,
  "os": nmap.nmap_os_detection,
  "subnet": nmap.nmap_subnet_scan,
  "top-port": nmap.scan_top_ports,
  "ver-detect": nmap.nmap_version_detection
}

def set_target_ports(target, nmap_res):
  """ Set target ports based on nmap result """

  nmap_ip_res = nmap_res.get(target.get_ip().get_address(), {})
  for p in nmap_ip_res.get("ports", []):
    product = p["service"].get("product", p["service"].get("name", "Unknown"))
    port = Port(int(p["portid"]), product, p.get("state", "opened"))
    target.get_ip().append_open_port(port)

def nmap(self, target, command = "ver-detect"):
  """ Perform an nmap scan on the target """

  if command not in nmap_commands.keys():
    raise ValueError(f"{command} is not a valid nmap command. Please use one of the following commands: \n{nmap_commands.keys()}")

  nmap_res = nmap_commands[command](target.get_ip().get_address())

  if command == "ver-detect":
    set_target_ports(target, nmap_res)
    target_ports = target.get_ip().get_port_strings()
    target_ports_list = "\n".join(target_ports)
    print(f"Found {len(target_ports)} ports on {target.get_domain()}:\n{target_ports_list}")

  return nmap_res
