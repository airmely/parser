import requests
from bs4 import BeautifulSoup
from dotenv import dotenv_values

ITEMS = 100
URL = dotenv_values('.env')['URL']


def function_that_parses_site():
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

    hh_request = requests.get(
        f'{URL}&items_on_page={ITEMS}',
        headers=headers,
    )

    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')

    pages = []

    paginator = hh_soup.find_all('span', {'class': 'pager-item-not-in-short-range'})

    for page in paginator:
        pages.append(int(page.find('a').text))


    return pages[-1]