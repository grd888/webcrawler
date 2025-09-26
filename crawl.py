from urllib.parse import urlparse

def normalize_url(url):
  parsed_url = urlparse(url)
  netloc = parsed_url.netloc 
  path = parsed_url.path
  if path.endswith('/'):
    path = path[:-1]
  return netloc + path