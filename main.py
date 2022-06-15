import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_link(link):
    link_get = requests.get(link)
    soup = BeautifulSoup(link_get.text, 'lxml')
    tovar = soup.find('div', class_='title_wrapper').find('h1').text
    high_price = soup.find('div', class_='price-tovar').find('div', class_='price-tovar-main').find('div', class_="price-tovar-new is_desktop").text
    try:
        low_price = soup.find('div', class_='price-tovar').find('div', class_='price-tovar-main').find('div',
                                                                                                       class_='price-tovar-old').text
    except:
        low_price = 0
    description = soup.find('div', class_='description_wrapper').text
    return tovar, high_price, low_price, description


data = pd.DataFrame(columns=['category', 'name', 'high_pricem', 'low_price', 'descriptions', 'link'])

respons = requests.get("https://tyumen.kolba.ru/")
soup = BeautifulSoup(respons.text, 'lxml')
category = soup.find('ul', class_='submenu').find_all('a')
for item in category:
    link = 'https://tyumen.kolba.ru' + item.get('href')
    category_name = item.text
    respons2 = requests.get(link)
    soup2 = BeautifulSoup(respons2.text, 'lxml')
    if soup2.find('ul', class_='products') != None:
        product = soup2.find('ul', class_='products').find_all('li')
        for p in product:
            link_p = 'https://tyumen.kolba.ru' + p.find('a').get('href')
            a = get_link(link_p)
            tmp = pd.DataFrame(data=[[category_name, a[0], a[1], a[2], a[3], link_p]], columns=data.columns)
            data = data.append(tmp)
            time.sleep(0.5)

    else:
        continue

data = data.reset_index(drop=True)
data.to_excel('colba.xls')
