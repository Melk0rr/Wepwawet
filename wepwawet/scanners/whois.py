import re
import requests

from bs4 import BeautifulSoup

from wepwawet.utils.color_print import ColorPrint
from wepwawet.utils.dictionary import join_dictionary_items

BASE_URL = "https://who.is/whois/"


def is_valid_row(row):
  """ Checks if a row is valid """
  return re.search(r'%|<|>', row) is None


def rows_2_dictionary(rows):
  """ Converts a list of rows into a dictionary """
  res = []
  s_index = -1
  for i in range(len(rows)):
    r = rows[i]
    # Create a new dictionary for each separator row
    if len(r) == 0:
      s_index += 1

      if i < len(rows) - 1:
        res.append({})

    # Append data to dictionaries based on the separator index
    else:
      key, value = r.split(":", maxsplit=1)

      # If the dictionary already contains the key : concatenate the two values
      f_value = value.strip()
      if key in res[s_index]:
        f_value = f"{res[s_index][key]}, {f_value}"

      res[s_index][key] = f_value

  return res


def whois(self, target):
  """ Parse data from who.is """

  url = f"{BASE_URL}{target.get_domain()}"

  try:
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

  except ConnectionError:
    ColorPrint.red(
        f"Could not connect to whois for domain {target.get_domain()}")

  try:
    raw_data = soup.find_all("pre")[0].text
    rows = [r for r in raw_data.split("\n") if is_valid_row(r)]
    data = rows_2_dictionary(rows)

    for dict in data:
      print(join_dictionary_items(dict, "\n"))
      print("\n")

  except:
    ColorPrint.red(f"No data found for {target.get_domain()}")
