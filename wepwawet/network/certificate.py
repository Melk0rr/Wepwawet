# INFO: Helper class to handle TLS certificate operations

from datetime import datetime
from typing import Any, Tuple

from wepwawet.utils.color_print import ColorPrint

"""

issued for
  Common name (CN)
  Organization (O)
  Organizational unit (OU)

issued by
  Common name (CN)
  Organization (O)
  Organizational unit (OU)

Validity period
  Issued on	vendredi 14 octobre 2022 à 02:00:00
  Expired on mercredi 15 novembre 2023 à 00:59:59


Footprints
  Footprint SHA-256	5F C5...
  Footprint SHA-1	88 A1...

{
  'subject': ((('commonName', ''),),),
  'issuer': (
              (('countryName', 'GB'),),
              (('stateOrProvinceName', ''),),
              (('localityName', ''),),
              (('organizationName', ''),),
              (('commonName', ''),)
            ),
  'version': x,
  'serialNumber': 'xxxxxxxxxxxxxxxxxxxxxxxxx',
  'notBefore': 'Oct 14 00:00:00 2022 GMT',
  'notAfter': 'Nov 14 23:59:59 2023 GMT',
  'subjectAltName': (('DNS', ''), ('DNS', '')),
  'OCSP': ('',),
  'caIssuers': ('file.crt',)}


"""


class Certificate:
    state = False
    code = -1
    reason = "[NONE]"
    message = "[NONE]"

    data = []
    validity = 0
    issued_for_cn = ""
    issued_for_o = ""

    def get_value(self, value: Tuple, parameter: str) -> Any:
        if type(value[0]) is tuple:
            return self.get_value(value[0], parameter)

        else:
            if value[0] == parameter:
                return value[1]

            else:
                return -1

    def analyse(self) -> bool:
        """Analyse certificate data"""
        res = False
        try:
            if self.state:
                self.validity = datetime.strptime(self.data["notAfter"], "%b %d %H:%M:%S %Y %Z")
                self.issued_for_cn = self.get_value(self.data["subject"], "commonName")
                self.issued_for_o = self.get_value(self.data["subject"], "organisation")
                res = True

        except Exception as err:
            ColorPrint.yellow(f"In {__class__.__name__} : {err} ")

        return res
