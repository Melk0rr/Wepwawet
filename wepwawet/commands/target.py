# INFO: Target module handling operations and data gathering on a list of targets

from multiprocessing import Pool
from typing import Dict, List

from wepwawet.network import URL
from wepwawet.scanners import (
    ask_shodan,
    check_header,
    check_tls,
    geoloc,
    http_info,
    nmap,
    ping,
    whois,
)
from wepwawet.utils import ColorPrint, export_csv, str_file_option_handle

from .base import Base

ip_track = {}


class Target(Base):
    """Main enumeration module"""

    def __init__(self, options: Dict) -> None:
        """Constructor"""
        super().__init__(options)

        self.results: List[Dict] = []
        self.unique_targets: List[URL] = []

        str_file_option_handle(self, "TARGET", "FILE")
        self.unique_targets = list(set(self.options["TARGET"]))
        print(f"Investigating {len(self.unique_targets)} hosts")
        print("Initializing...")

        # Cleanup targets and init instances
        unique_urls = []
        with Pool(processes=10) as pool:
            for url in pool.map(self.init_url, self.unique_targets):
                unique_urls.append(url)

        self.unique_targets: List[URL] = unique_urls

    def init_url(self, target: str) -> URL:
        """Init url instance based on target index and resolve ip address"""
        url = URL(target)
        url.resolve_ip()

        return url

    def handle_exception(self, e, message="") -> None:
        """Function handling exception for the current class"""
        if self.options["--verbose"]:
            print(e)

        if message:
            ColorPrint.red(message)

    def url_process(self, target: URL) -> Dict:
        """Target process to deal with url data"""
        options_res = {}
        target_ip = target.get_ip_str()

        # NOTE: Ping
        if self.options["--ping"]:
            respond = ping(self, target)
            options_res.update({"ping": "YES" if respond else "NO"})

        # NOTE: Shodan
        if self.options["--shodan"]:
            options_res.update(ask_shodan(self, target))

        # NOTE: Http
        if self.options["--http-info"]:
            options_res.update(http_info(self, target))

        # NOTE: Geolocate
        if self.options["--geo-locate"]:
            geoloc(self, target)

        # NOTE: Nmap
        if self.options["--nmap"]:
            # INFO: Try to gain some time => check if the ip was already scanned (some url may share same ip)
            if target_ip not in ip_track:
                nmap(self, target)
                ip_track[target_ip] = target.get_ip_str()

            else:
                print(f"{target.get_domain()} IP was already scanned. Skipping...")
                target.set_ip(ip_track[target_ip])

        # NOTE: TLS
        if self.options["--check-tls"]:
            print("\nGathering additional information from https TLS acceptance...")
            options_res.update(check_header(target))
            options_res.update(check_tls(target))

        # NOTE: Whois
        if self.options["--whois"]:
            print("\nChecking Who.is...")
            whois(self, target)

        return {**target.to_dictionary(), **options_res}

    def run(self) -> None:
        print("\nProcessing targets...")
        # Retreive IP of target and run initial configuration
        with Pool(processes=10) as pool:
            for url_data in pool.imap_unordered(self.url_process, self.unique_targets):
                self.results.append(url_data)

        # Export results to CSV if option is provided
        if self.options["--export-csv"]:
            export_csv()
