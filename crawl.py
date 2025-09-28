from urllib.parse import urljoin, urlparse
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
  
def get_urls_from_html(html, base_url):
  soup = BeautifulSoup(html, 'html.parser')
  urls = []
  for link in soup.find_all('a'):
    href = link.get('href')
    if href.startswith('/'):
      urls.append(urljoin(base_url, href))
    else:
      urls.append(href) 
  return urls
      
def get_images_from_html(html, base_url):
  soup = BeautifulSoup(html, 'html.parser')
  images = []
  for image in soup.find_all('img'):
    src = image.get('src')
    if src is None:
      continue
    if src and src.startswith('/'):
      images.append(urljoin(base_url, src))
    elif src:
      images.append(src) 
  return images
  