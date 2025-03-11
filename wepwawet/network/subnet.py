# INFO: Helper class to handle subnets
from typing import Dict, List, Union

from oudjat.utils import i_and, i_or

from .ipv4 import IPv4, IPv4Mask, ip_int_to_str


class Subnet:
    """A class to handle subnets"""

    # ****************************************************************
    # Attributes & Constructors

    def __init__(
        self,
        address: Union[str, IPv4],
        name: str,
        mask: Union[int, str, IPv4Mask] = None,
        description: str = None,
        hosts: Union[List[IPv4], List[str]] = None,
    ):
        """Constructor"""

        self.mask: IPv4Mask = None

        # INFO: Try to extract mask if provided as CIDR notation
        cidr = None
        if (type(address) is str) and ("/" in address):
            address, cidr = address.split("/")
            cidr = int(cidr)

            if cidr is not None:
                mask = IPv4Mask.get_netmask(cidr)

        if not isinstance(address, IPv4):
            address = IPv4(address)

        if mask is None:
            raise ValueError(
                f"Subnet::Provided net address has no mask set: {address.get_address()}"
            )

        self.set_mask(mask)

        self.address: IPv4 = IPv4(address=i_and(int(address), int(self.mask)))
        self.broadcast = self.get_broadcast_address()

        self.name = name
        self.description = description

        self.hosts = {}

        if hosts is not None:
            for ip in hosts:
                self.add_host(ip)

    # ****************************************************************
    # Methods

    def get_name(self) -> str:
        """Getter for the subnet name"""
        return self.name

    def get_description(self) -> str:
        """Getter for the subnet description"""
        return self.description

    def get_address(self) -> IPv4:
        """Getter for subnet address"""
        return self.address

    def get_mask(self) -> IPv4Mask:
        """Getter for ip mask instance"""
        return self.mask

    def get_broadcast_address(self) -> IPv4:
        """Returns the broadcast address of the current subnet"""
        return IPv4(ip_int_to_str(i_or(int(self.mask.get_wildcard()), int(self.address))))

    def set_mask(self, mask: Union[int, str, IPv4Mask]) -> None:
        """Setter for ip mask"""

        if not isinstance(mask, IPv4Mask):
            mask = IPv4Mask(mask)

        self.mask = mask

    def contains(self, ip: Union[str, IPv4]) -> bool:
        """Checks wheither the provided IP is in the current subnet"""
        if not isinstance(ip, IPv4):
            ip = IPv4(ip)

        mask_address = int(self.mask)
        return i_and(int(ip), mask_address) == i_and(int(self.address), mask_address)

    def list_addresses(self) -> List[str]:
        """Lists all possible hosts in subnet"""

        # NOTE: Starts with first address after subnet addres
        # Ends with broadcast address
        start = self.address.get_address() + 1
        end = self.broadcast.get_address()

        return [f"{ip_int_to_str(i)}/{self.mask.get_cidr()}" for i in range(start, end)]

    def add_host(self, host: Union[str, IPv4]) -> None:
        """Adds a new host to the subnet"""

        if not isinstance(host, IPv4):
            host = IPv4(host)

        # NOTE: Checks if the address is not the subnet address nor the broadcast one
        if (
            self.contains(host)
            and (int(host) != int(self.address))
            and (int(host) != int(self.broadcast))
        ):
            self.hosts[str(host)] = host

    # INFO: Convertion methods
    def __str__(self) -> str:
        """Returns a string based on current instance"""
        return f"{self.address}/{self.mask.get_cidr()}"

    def to_dict(self) -> Dict:
        """Converts the current subnet instance into a dictionary"""

        return {
            "net_address": str(self.get_address()),
            "net_mask": str(self.get_mask()),
            "net_mask_cidr": self.get_mask().__str__(as_cidr=True),
            "hosts": self.hosts,
            "broadcast_address": str(self.get_broadcast_address()),
        }

