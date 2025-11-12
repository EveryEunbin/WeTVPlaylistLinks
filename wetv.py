from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import csv
import csv
import json
from bs4 import BeautifulSoup
from urllib.parse import parse_qs

options = Options()
options.add_argument("--headless")

url = 'https://wetv.vip/th/play/n6ihq5rynbdi1ae/b4101fq016y'

driver = webdriver.Firefox(options=options)
driver.get(url)
title_name = driver.title
title_part, _ = title_name.split('-', 1)
_, serie_name = title_part.split(" ", 1)
serie_name = serie_name.strip()

tabs = driver.find_elements(By.CSS_SELECTOR, ".index-tab-item")
ep = 0
titles = []
links = []



for tab in tabs:
    driver.execute_script("arguments[0].click();", tab)
    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, 'html.parser')
    all_li = soup.select('li.play-video__item')
    
    for li in all_li:
        query_dict = parse_qs(li['dt-params'])
        url = f'https://wetv.vip/th/play/{query_dict['cid'][0]}/{query_dict['vid'][0]}'
        ep = ep + 1
        title = f'EP{str(ep).zfill(2)} {serie_name}'
        titles.append(title)
        links.append(url) 
    
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
