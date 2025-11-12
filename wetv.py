import requests
import csv
import json
from bs4 import BeautifulSoup

title_search = 'เกมรักในเงาลวง'
url = f'https://wetv.vip/th/search/{title_search}'
main_url = 'https://wetv.vip'
titles = []
links = []

r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc, 'html.parser')
names_soup = soup.select('.search-result__title>span:first-child')
main_titles = [name.get_text() for name in names_soup]

uls = soup.select('ul.search-result__videos')

if len(uls)==len(main_titles):
    for i, ul in enumerate(uls):
        all_a = ul.select('a.search-result__link')
        for a_tag in all_a:
            title = f'EP{a_tag['title']} {main_titles[i]}'
            link = f'{main_url}{a_tag['href']}'
            titles.append(title)
            links.append(link)
else:
    print('Cannot process')

with open('links.csv', 'w', newline='') as csvfile:
    fieldnames = ['title', 'link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(titles)):
        writer.writerow({'title': titles[i], 'link': links[i]})

with open('links.csv', mode='r', newline='') as csvfile:
    data = list(csv.DictReader(csvfile))

with open('links.json', mode='w') as jsonfile:
    json.dump(data, jsonfile, indent=4, ensure_ascii=False)
