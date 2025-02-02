""" HTTP plugin used to check basic http infos for a given target """
import requests

from typing import Dict
from bs4 import BeautifulSoup

def http_info(self, target: "URL") -> Dict:
  """ Performs a simple HTTP request to the given target """

  http_status = http_title = ""

  print(f"{target.get_domain()}, getting HTTP infos", end="...")

  try:
    req = requests.get(target.get_host())
    soup = BeautifulSoup(req.content, 'html.parser')

    http_status = req.status_code
    http_title = soup.title.text.replace("\n", "").replace("\t", " ")

    print(f"{http_title} ({http_status})")

  except Exception as e:
    self.handle_exception(
        e, f"Error while requesting {target.get_domain()}. Make sure the target is accessible")

  return {
      "http_status": http_status,
      "http_title": http_title
  }
