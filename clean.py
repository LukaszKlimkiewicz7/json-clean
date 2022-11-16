import json
from bs4 import BeautifulSoup, Comment

VALID_TAGS = ['span', 'div', 'p']

def clean_xml(xml_text):
  if 'OfficeDocumentSettings' in xml_text:
    return clean_word_xml(xml_text)
  else:
    return clean_standard_xml(xml_text)

def clean_word_xml(xml_text):
  soup = BeautifulSoup(xml_text, "lxml")
  _remove_comments(soup)
  _remove_invalid_tags(soup)
  _remove_class_and_style(soup)
  return str(soup).replace("<html><body>","").replace("</body></html>","")

def clean_standard_xml(xml_text):
  soup = BeautifulSoup(xml_text, "lxml")
  _remove_class_and_style(soup)
  _remove_word_styles(soup)
  return str(soup).replace("<html><body>","").replace("</body></html>","")

def _remove_comments(soup):
  comments = soup.find_all(string=lambda text: isinstance(text, Comment))
  for c in comments:
    c.extract()

def _remove_invalid_tags(soup):
  tags = soup.select(f":not({','.join(VALID_TAGS)})")
  for tag in tags:
    tag.unwrap()

def _remove_class_and_style(soup):
  for tag in soup.find_all():
    del tag["class"]
    del tag["id"]

def _remove_word_styles(soup):
  for tag in soup.find_all():
    if 'style' in tag.attrs:
      style = tag['style']
      attrs = style.split(';')
      filtered_attrs = [attr for attr in attrs if not attr.strip().startswith('mso')]
      filtered_style = ';'.join(filtered_attrs)
      tag['style'] = filtered_style
