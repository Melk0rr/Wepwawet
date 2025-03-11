from typing import TYPE_CHECKING, Dict

import requests
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from wepwawet.network.url import URL

def http_info(self, target: "URL", allow_redirects: bool = False) -> Dict:
    """Performs a simple HTTP request to the given target"""

    http_status = None
    http_title = None

    print(f"{target.get_domain()}, getting HTTP infos", end="...")

    try:
        req = requests.get(target.get_host(), allow_redirects=allow_redirects)
        soup = BeautifulSoup(req.content, "html.parser")

        http_status = req.status_code
        http_title = soup.title.text.replace("\n", "").replace("\t", " ")

        print(f"{http_title} ({http_status})")

    except Exception as e:
        self.handle_exception(
            e, f"Error while requesting {target.get_domain()}. Make sure the target is accessible"
        )

    return {"http_status": http_status, "http_title": http_title}
