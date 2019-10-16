import re

from bs4 import BeautifulSoup


def html_to_str(html, break_line=False):
    soup = BeautifulSoup(html, 'html.parser')
    result = ''
    for paragraph in soup.find_all('p'):
        result += (paragraph.get_text().strip() + '\n')
    if not break_line:
        result = result.replace('\n', ' ')
    return result.strip()


def upper_camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
