""" HTTP plugin used to check basic http infos for a given target """
import requests
from bs4 import BeautifulSoup


def http_info(self, target):
  """ Performs a simple HTTP request to the given target """

  http_status = http_title = ""
  print(f"\nRequesting {target.get_domain()}...")

  try:
    req = requests.get(target.get_host())
    soup = BeautifulSoup(req.content, 'html.parser')

    http_status = req.status_code
    http_title = soup.title.text.replace("\n", "").replace("\t", " ")

  except Exception as e:
    self.handle_exception(
        e, f"Error while requesting {target.get_domain()}. Make sure the target is accessible")

  print(f"HTTP status: {http_status}, HTTP title: {http_title}")

  return {
      "http_status": http_status,
      "http_title": http_title
  }
