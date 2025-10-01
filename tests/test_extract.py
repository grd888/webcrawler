import unittest
from crawl import get_h1_from_html, get_first_paragraph_from_html

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
    
  def test_get_first_paragraph_from_html_main_priority(self):
    input_body = '''<html><body>
        <p>Outside paragraph.</p>
        <main>
            <p>Main paragraph.</p>
        </main>
    </body></html>'''
    actual = get_first_paragraph_from_html(input_body)
    expected = "Main paragraph."
    self.assertEqual(actual, expected)
    
  def test_get_first_paragraph_from_html_no_main_priority(self):
    input_body = '''<html><body>
        <p>1st paragraph.</p>
        
        <p>2nd paragraph.</p>
        
    </body></html>'''
    actual = get_first_paragraph_from_html(input_body)
    expected = "1st paragraph."
    self.assertEqual(actual, expected)
    
  def test_get_first_paragraph_from_html_no_paragraph(self):
    input_body = '''<html><body>
        <main>
            <h1>1st paragraph.</h1>
        </main>
    </body></html>'''
    actual = get_first_paragraph_from_html(input_body)
    expected = ""
    self.assertEqual(actual, expected)


