from scanners.lookup import nslookup
from scanners.shodan import ask_shodan

def main():
  with open('./src/urls.txt', encoding='utf-8') as f: lines = f.readlines()

  for url in lines:
    ip = nslookup(url)