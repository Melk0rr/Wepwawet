# INFO: Target module handling operations and data gathering on a list of targets

import csv
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
from wepwawet.utils import ColorPrint, str_file_option_handle

from .base import Base

ip_track = {}


class Target(Base):
    """Main enumeration module"""

    def __init__(self, options: Dict):
        """Constructor"""
        super().__init__(options)

        self.results: List[Dict] = []
        self.unique_targets: List[URL] = []

        str_file_option_handle(self, "TARGET", "FILE")
        self.unique_targets = list(set(self.options["TARGET"]))
        print(f"Investigating {len(self.unique_targets)} hosts")
        print("Initializing...")

        # Clean up targets and init instances
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

    def export_csv(self) -> None:
        """Write the results into a CSV file"""
        print("\nExporting results to csv...")

        if len(self.results) <= 0:
            ColorPrint.red(f"Error while exporting results to CSV: ({len(self.results)} results)s")
            return 0

        try:
            with open(self.options["--export-csv"], "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys(), delimiter="|")
                writer.writeheader()
                writer.writerows(self.results)

        except Exception as e:
            ColorPrint.red(f"{__class__.__name__} : {e} cannot save to CSV")

    def url_process(self, target: URL) -> Dict:
        """Target process to deal with url data"""
        options_res = {}
        target_ip = target.get_ip_str()
        # If option is provided run ping on the target
        if self.options["--ping"]:
            respond = ping(self, target)
            options_res.update({"ping": "YES" if respond else "NO"})

        # If option is provided: check for informations with shodan API
        if self.options["--shodan"]:
            options_res.update(ask_shodan(self, target))

        # If option is provided: do a simple http request to the target to retreive status and title
        if self.options["--http-info"]:
            options_res.update(http_info(self, target))

        # If option is provided: geo locate the target
        if self.options["--geo-locate"]:
            geoloc(self, target)

        # If option is provided: scan target with nmap
        if self.options["--nmap"]:
            # Check if the ip was already scanned (some url may share same ip)
            if target_ip not in ip_track:
                nmap(self, target)
                ip_track[target_ip] = target.get_ip_str()

            else:
                print(f"{target.get_domain()} IP was already scanned. Skipping...")
                target.set_ip(ip_track[target_ip])

        # If option is provided: do a simple check to the target to retreive TLS status
        if self.options["--check-tls"]:
            print("\nGathering additional information from https TLS acceptance...")
            options_res.update(check_header(target))
            options_res.update(check_tls(target))

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
            self.export_csv()

