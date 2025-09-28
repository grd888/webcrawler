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