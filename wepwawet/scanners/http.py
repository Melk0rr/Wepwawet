import requests
from bs4 import BeautifulSoup

def http_info(self, target):
  req = requests.get(target)
  soup = BeautifulSoup(req.content)

  target_index = self.options["TARGET"].index(target)

  self.urls[target_index] = { 
    **self.urls[target_index],
    "http_status": req.status_code,
    "http_title": soup.title.text
  }