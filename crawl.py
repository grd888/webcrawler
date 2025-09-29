from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
  parsed_url = urlparse(url)
  netloc = parsed_url.netloc 
  path = parsed_url.path
  full_path = netloc + path
  full_path = full_path.rstrip("/")
  return full_path

def get_h1_from_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  h1 = soup.find('h1')
  return h1.get_text(strip=True) if h1 else ""

def get_first_paragraph_from_html(html):
  soup = BeautifulSoup(html, 'html.parser')
  main = soup.find('main')
  if main:
    p = main.find('p')
  else:
    p =soup.find('p')
    
  return p.get_text(strip=True) if p else ""
  
  
def get_urls_from_html(html, base_url):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")

    for anchor in anchors:
        if href := anchor.get("href"):
            try:
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {href}")

    return urls


def get_images_from_html(html, base_url):
    image_urls = []
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        if src := img.get("src"):
            try:
                absolute_url = urljoin(base_url, src)
                image_urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {src}")

    return image_urls