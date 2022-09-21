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

  print(f"\nRequesting {host}...")

  try:
    req = requests.get(host)
    soup = BeautifulSoup(req.content, 'html.parser')

    http_status = req.status_code
    http_title = soup.title.text

    print(f"HTTP status: {http_status}, HTTP title: {http_title}")

  except Exception as e:
    self.handle_exception(e, f"Error while requesting {host}. Make sure the target is accessible")

  target_index = self.options["TARGET"].index(target)

  self.urls[target_index] = {
    **self.urls[target_index],
    "http_status": http_status,
    "http_title": http_title
  }
