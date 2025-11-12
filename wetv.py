from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import json
import time

options = Options()
options.add_argument("-headless")

title_search = 'ดาราจักรรักลำนำใจ'
url = f'https://wetv.vip/th/search/{title_search}'
main_url = 'https://wetv.vip'
titles = []
links = []

driver = webdriver.Firefox(options=options)
driver.get(url)

collapses = driver.find_elements(By.CSS_SELECTOR, "li.search-result__video--collapse")
if len(collapses)>0:
    print('Having Collapse(s)')
    for collapse in collapses:
        driver.execute_script("arguments[0].click();", collapse)
        time.sleep(3)

html_doc = driver.page_source
soup = BeautifulSoup(html_doc, 'html.parser')
names_soup = soup.select('.search-result__title>span:first-child')
main_titles = [name.get_text() for name in names_soup]

uls = soup.select('ul.search-result__videos')

if len(uls)==len(main_titles):
    for i, ul in enumerate(uls):
        print(main_titles[i])
        all_a = ul.select('a.search-result__link')
        for a_tag in all_a:
            title = f'EP{a_tag['title']} {main_titles[i]}'
            link = f'{main_url}{a_tag['href']}'
            titles.append(title)
            links.append(link)
else:
    print('Cannot process')

driver.quit()

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
