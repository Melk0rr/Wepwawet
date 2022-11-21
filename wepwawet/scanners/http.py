""" HTTP plugin used to check basic http infos for a given target """
import requests
from bs4 import BeautifulSoup

def http_info(self, target_index):
  """ Performs a simple HTTP request to the given target """
  target = self.urls[target_index]
  host = target["host"]
  http_status = http_title = ""

  print(f"\nRequesting {host}...")

  try:
    req = requests.get(host)
    soup = BeautifulSoup(req.content, 'html.parser')

  except Exception as e:
    self.handle_exception(e, f"Error while requesting {host}. Make sure the target is accessible")

  http_status = req.status_code
  http_title = soup.title.text

  print(f"HTTP status: {http_status}, HTTP title: {http_title}")

  self.urls[target_index] = {
    **target,
    "http_status": http_status,
    "http_title": http_title
  }
