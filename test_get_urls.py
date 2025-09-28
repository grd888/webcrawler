import unittest
from crawl import get_urls_from_html

class TestGetUrls(unittest.TestCase):
  def test_get_urls_from_html_absolute(self):
    input_url = "https://blog.boot.dev"
    input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
    actual = get_urls_from_html(input_body, input_url)
    expected = ["https://blog.boot.dev"]
    self.assertEqual(actual, expected)
    
  def test_get_urls_from_html_relative(self):
    input_url = "https://blog.boot.dev"
    input_body = '<html><body><a href="/about"><span>About</span></a></body></html>'
    actual = get_urls_from_html(input_body, input_url)
    expected = ["https://blog.boot.dev/about"]
    self.assertEqual(actual, expected)