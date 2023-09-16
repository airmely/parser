import requests

from bs4 import BeautifulSoup
from dotenv import dotenv_values


URL = dotenv_values('.env')['URL']

headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

def function_that_parses_site():
    hh_request = requests.get(
        URL,
        headers=headers,
    )

    hh_soup = BeautifulSoup(
        hh_request.text,
        'html.parser'
        )

    paginator = hh_soup.find_all(
        'span', 
        {'class': 'pager-item-not-in-short-range'}
        )
    
    pages = []

    for page in paginator:
        pages.append(int(page.find('a').text))


    return pages[-1]

def processing_function(html):
    title = html.find('a').text
    link = html.find('a')['href']
    add_info = html.find(
        'div', 
        {'class': 'vacancy-serp-item__meta-info-company'}
        ).find('a').text
    add_info = add_info.strip()
    location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.split()[0].replace(',', '')
    
    return {
        'title': title,
        'add_info': add_info,
        'location': location,
        'link': link,
    }

def extract_site_info(last_page):
    info = []

    # for page in range(last_page):
    result = requests.get(
        URL,
        headers=headers,
        )

    soup = BeautifulSoup(
        result.text,
        'html.parser'
        )
    
    results = soup.find_all('div', {'class' : 'serp-item'})

    for result in results:
        page = processing_function(result)
        info.append(page)

    return info


def get_info():
    max_page = function_that_parses_site()
    result = extract_site_info(max_page)
    return result