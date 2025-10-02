import unittest
from crawl import get_images_from_html

class TestGetImages(unittest.TestCase):
  def test_get_images_from_html_relative(self):
    input_url = "https://blog.boot.dev"
    input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
    actual = get_images_from_html(input_body, input_url)
    expected = ["https://blog.boot.dev/logo.png"]
    self.assertEqual(actual, expected)
    
  def test_get_images_from_html_absolute(self):
    input_url = "https://blog.boot.dev"
    input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Logo"></body></html>'
    actual = get_images_from_html(input_body, input_url)
    expected = ["https://blog.boot.dev/logo.png"]
    self.assertEqual(actual, expected)
    
  def test_get_images_from_html_no_images(self):
    input_url = "https://blog.boot.dev"
    input_body = '<html><body></body></html>'
    actual = get_images_from_html(input_body, input_url)
    expected = []
    self.assertEqual(actual, expected)
    
  def test_get_images_from_html_missing_attributes(self):
    input_url = "https://blog.boot.dev"
    input_body = '<html><body><img alt="Logo"></body></html>'
    actual = get_images_from_html(input_body, input_url)
    expected = []
    self.assertEqual(actual, expected)
    
    
  