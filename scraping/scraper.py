from re import split
import requests
import json
import os

from bs4 import BeautifulSoup

data = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 OPR/75.0.3969.267'}

pages = {
    "Semanario": "https://semanariouniversidad.com/ultima-hora/",
    "Amelia": "https://www.ameliarueda.com/noticias-costa-rica",
    "Mundo": "https://www.elmundo.cr/costa-rica/",
    "Sinart": "https://costaricamedios.cr/noticias/"
}


actual_path = os.path.dirname(os.path.abspath(__file__))
scrape_result_path = actual_path + "/scrape_result.json"

def removeUnicode(text):
    with open("unicode.json") as f:
        codes = json.load(f)
        unicodes = list(codes.keys())

        for u in unicodes:
            text = text.replace(u, codes[u])

    return text

def scrapSemanario(page, r):
    soup = BeautifulSoup(r.text, 'html.parser')
    data[page] = []

    articles = soup.find_all('article', class_='post')

    for article in articles:
        link = article.div.h2.a
        try:
            url = link['href']
        except:
            break

        response = requests.get(url, headers=headers)
        article_soup = BeautifulSoup(response.text, 'html.parser')

        header = article_soup.find('div', class_='entry-header')
        content = article_soup.find('div', class_='contenido-textual')
        time = article_soup.find('time', class_='updated')
        img = article_soup.find('img', class_='wp-post-image')
        
        data_content = {}
        data_content["headline"] = removeUnicode(header.h1.text)
        data_content["article"] = removeUnicode(content.text)
        data_content["time"] = time.text.strip()
        data_content["img"] = img["data-lazy-src"]

        data[page].append(data_content)


def scrapAmelia(page, r):
    soup = BeautifulSoup(r.text, 'html.parser')
    data[page] = []

    articles = soup.find_all('article', class_='ar-list-entry')

    for i, article in enumerate(articles):
        link = article.div.a
        try:
            url = link['href']
        except:
            break

        url = 'https://www.ameliarueda.com' + url
        response = requests.get(url, headers=headers)
        article_soup = BeautifulSoup(response.text, 'html.parser')

        header = article_soup.find('h1', class_='ar-entry__title')
        content = article_soup.find('div', class_='ar-entry__text')
        time = article_soup.find('p', class_='ar-entry__date')
        img = soup.find_all('img', class_='ar-list-entry__img')[i]

        data_content = {}
        data_content["headline"] = removeUnicode(header.text)
        data_content["article"] = removeUnicode(content.text)
        data_content["time"] = time.text.strip()
        data_content["img"] = img["src"].strip()

        data[page].append(data_content)


def replaceGarbageMundo(text):
    splitted = text.split('(elmundo.cr)')

    time = splitted[0]
    text = splitted[1]
    
    splitted = text.split('.')
    garbage = splitted[-1]

    replaced = text.replace(garbage, '')
    article = removeUnicode(replaced.strip())

    return article, time

def scrapMundo(page, r):
    soup = BeautifulSoup(r.text, 'html.parser')
    data[page] = []

    articles = soup.find_all('article', class_='format-standard')

    for article in articles:
        link = article.h3.a
        try:
            url = link['href']
        except:
            break

        response = requests.get(url, headers=headers)
        article_soup = BeautifulSoup(response.text, 'html.parser')

        header = article_soup.find('h1', class_='entry-title')
        content = article_soup.find('div', class_='entry-content')
        img = article_soup.find('img', class_='size-full')

        img_res = requests.get(img['data-permalink'], headers=headers)
        image_soup = BeautifulSoup(img_res.text, 'html.parser')

        img = image_soup.find('img', class_='attachment-medium')

        data_content = {}
        data_content["headline"] = removeUnicode(header.text)
        data_content["article"], data_content["time"] = replaceGarbageMundo(content.text[212:])
        if img:
            data_content["img"] = 'https://www.elmundo.cr' + img["src"]

        data[page].append(data_content)

def replaceGarbageSinart(text):
    splitted = text.split('.')

    garbage = splitted[-1]
    replaced = text.replace(garbage, '')
    article = removeUnicode(replaced.strip())

    return article


def scrapSinart(page, r):
    soup = BeautifulSoup(r.text, 'html.parser')
    data[page] = []

    articles = soup.find_all('div', class_='item-details')

    for article in articles:
        link = article.h3.a
        try:
            url = link['href']
        except:
            break

        response = requests.get(url, headers=headers)
        article_soup = BeautifulSoup(response.text, 'html.parser')

        header = article_soup.find('h1', class_='entry-title')
        content = article_soup.find('div', class_='td-post-content')
        time = article_soup.find('time',class_='entry-date')
        img = article_soup.find('img', class_='entry-thumb')

        data_content = {}
        data_content["headline"] = removeUnicode(header.text)
        data_content["article"] = replaceGarbageSinart(content.text) 
        data_content["time"] = time.text
        data_content["img"] = img["src"]

        year = data_content["time"].split(',')[1]
        if year == ' 2021':
            data[page].append(data_content)


def doScraping():
    print("Inicia Scraping")
    for key, value in pages.items():
        print("Scrapeando: " + str(key) + " - "+str(value))
        r = requests.get(value, headers=headers)
        if key == "Semanario":
            scrapSemanario(key, r)
        elif key == "Amelia":
            scrapAmelia(key, r)
        elif key == "Mundo":
            scrapMundo(key, r)
        elif key == "Sinart":
            scrapSinart(key, r)
            
    with open(scrape_result_path, 'w') as json_file:
        json.dump(data, json_file)



