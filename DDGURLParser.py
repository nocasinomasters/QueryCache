import HTMLParser

# crawl a duckduckgo results page for divs containing URLs
class DDGURLParser(HTMLParser.HTMLParser):
  def __init__(self):
    HTMLParser.HTMLParser.__init__(self)
    self.recording = 0
    self.data = []

  def handle_starttag(self, tag, attributes):
    if tag == 'a':
      for name, value in attributes:
        if name == 'href' and value.startswith('http'):
          self.data.append(value)

  def handle_endtag(self, tag):
    pass

  def handle_data(self, data):
    pass
