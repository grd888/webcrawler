import unittest
from crawl import extract_page_data

class TestGetPage(unittest.TestCase):
  def test_extract_page_data_basic(self):
    input_url = "https://blog.boot.dev"
    input_body = '''<html><body>
        <h1>Test Title</h1>
        <p>This is the first paragraph.</p>
        <a href="/link1">Link 1</a>
        <img src="/image1.jpg" alt="Image 1">
    </body></html>'''
    actual = extract_page_data(input_body, input_url)
    expected = {
        "url": "https://blog.boot.dev",
        "h1": "Test Title",
        "first_paragraph": "This is the first paragraph.",
        "outgoing_links": ["https://blog.boot.dev/link1"],
        "image_urls": ["https://blog.boot.dev/image1.jpg"]
    }
    self.assertEqual(actual, expected)