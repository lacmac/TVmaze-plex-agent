from bs4 import BeautifulSoup


def strip_tags(string):
    if string is None or string == '':
        return ''
    return BeautifulSoup(string, 'html.parser').get_text()
