from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
  parsed_url = urlparse(url)
  netloc = parsed_url.netloc 
  path = parsed_url.path
  if path.endswith('/'):
    path = path[:-1]
  return netloc + path

def get_h1_from_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  h1 = soup.find('h1')
  return h1.get_text() if h1 else ""

def get_first_paragraph_from_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  main = soup.find('main')
  if main:
    p = main.find('p')
    if p:
      return p.get_text()
    else:
      return ""
  elif soup.find('p'):
    return soup.find('p').get_text()
  else:
    return ""