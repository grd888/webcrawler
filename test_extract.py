import unittest
from crawl import get_h1_from_html

class TestExtract(unittest.TestCase):
  def test_get_h1_from_html1(self):
    html = """
    <html>
      <head>
        <title>Test Page</title>
      </head>
      <body>
        <h1>Test H1</h1>
      </body>
    </html>
    """
    actual = get_h1_from_html(html)
    expected = "Test H1"
    self.assertEqual(actual, expected)
    
  def test_get_h1_from_html2(self):
    html = """
    <html>
      <head>
        <title>Test Page</title>
      </head>
      <body>
        <h1>Test H1</h1>
        <h2>Test H2</h2>
      </body>
    </html>
    """
    actual = get_h1_from_html(html)
    expected = "Test H1"
    self.assertEqual(actual, expected)
    
  def test_get_h1_from_html3(self):
    html = """
    <html>
      <head>
        <title>Test Page</title>
      </head>
      <body>
        <h2>Test H2</h2>
      </body>
    </html>
    """
    actual = get_h1_from_html(html)
    expected = ""
    self.assertEqual(actual, expected)


