from bs4 import BeautifulSoup as BS
import requests


def get_river():
    response = requests.get('https://www.wpws.kr/hangang/')
    html = response.text
    soup = BS(html, 'html.parser')

    for tag in soup.select('#temp'):
        a = tag.text

    return a
