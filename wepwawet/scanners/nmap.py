# INFO: Module to perform nmap scans on URL and IP addresses

from typing import TYPE_CHECKING, Dict

import nmap3

from wepwawet.network.port import Port
from wepwawet.utils.color_print import ColorPrint

if TYPE_CHECKING:
    from wepwawet.network.url import URL

nmap = nmap3.Nmap()

# INFO: Nmap command switch
nmap_commands = {
    "dns-brute": nmap.nmap_dns_brute_script,
    "os": nmap.nmap_os_detection,
    "subnet": nmap.nmap_subnet_scan,
    "top-port": nmap.scan_top_ports,
    "ver-detect": nmap.nmap_version_detection,
}


def set_target_ports(target, nmap_res: Dict) -> None:
    """Set target ports based on nmap result"""

    nmap_ip_res = nmap_res.get(str(target.get_ip()), {})
    for p in nmap_ip_res.get("ports", []):
        product = p["service"].get("product", p["service"].get("name", "Unknown"))
        port = Port(int(p["portid"]), product, p.get("state", "opened"))
        target.get_ip().append_open_port(port)


def nmap(self, target: "URL", command: str = "ver-detect") -> Dict:
    """Perform an nmap scan on the target"""

    if command not in nmap_commands.keys():
        raise ValueError(
            f"{command} is not a valid nmap command. Please use one of the following commands: \n{nmap_commands.keys()}"
        )

    nmap_res = None

    if target.get_ip() is not None:
        print(f"Scanning {target.get_domain()} with nmap", end="...")

        nmap_res = nmap_commands[command](target.get_ip().get_address())

        # TODO: Handle various command behaviors
        if command == "ver-detect":
            set_target_ports(target, nmap_res)
            target_ports = target.get_ip().get_port_strings()
            target_ports_list = "\n".join(target_ports)
            print(f"Found {len(target_ports)} ports on {target.get_domain()}:\n{target_ports_list}")

    else:
        ColorPrint.red(f"No ip to scan for {target.get_domain()}")

    return nmap_res
