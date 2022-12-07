""" HTTP plugin used to check basic http infos for a given target """
import re

import requests
from bs4 import BeautifulSoup


def http_info(self, target):
  """ Performs a simple HTTP request to the given target """

  host = target["host"]

  if not re.match(r'http(s?):', host):
    host = 'http://' + target["host"]

  http_status = http_title = ""
  print(f"\nRequesting {target['host']}...")

  try:
    req = requests.get(host)
    soup = BeautifulSoup(req.content, 'html.parser')

    http_status = req.status_code
    http_title = soup.title.text

  except Exception as e:
    self.handle_exception(
        e, f"Error while requesting {target['host']}. Make sure the target is accessible")

  print(f"HTTP status: {http_status}, HTTP title: {http_title}")

  return {
      "http_status": http_status,
      "http_title": http_title
  }
