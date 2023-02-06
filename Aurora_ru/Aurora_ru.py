import requests
from bs4 import BeautifulSoup
import csv
import os
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
          'Accept': 'ext/html,application/xhtml+txml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}

# test на файле
# with open('all.htm', encoding='utf-8') as file:
#     text = file.read()
#     soup = BeautifulSoup(text, 'lxml')

file_name = input('Введите название файла для сохранения:  ') + '.csv'
with open(file_name, 'w', encoding='utf-8', newline='') as file_csv:
    writer = csv.writer(file_csv, delimiter=';')
    writer.writerow(['Наименование', 'Артикул', 'Цена', 'Описание', 'Характеристики', 'Ссылка'])

# Получение URL товаров со странички
# url = input('Введите URL для опроса')
url = f'https://aurora.ru/catalog/category/aksessuary-dlya-shitya/'
response = requests.get(url=url, headers=header)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

# Получаем список URL
links = [i.next['href'] for i in soup.find_all('div', class_="catalog_item_name")]
print(links)

# test на файле
# with open('Aurora_ru/one.htm', encoding='utf-8') as file:
#     text = file.read()
#     soup = BeautifulSoup(text, 'lxml')


for link in links:
    link = f'https://aurora.ru{link}'
    response = requests.get(url=link, headers=header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    names = [i.text.strip() for i in soup.find('h1', class_="goods_h1_name")]
    articles = [i.text.split(':')[1].strip() for i in soup.find('div', class_="goods_artikul")]
    prices = [''.join(i.text.split()).strip() for i in soup.find('span', class_="price")]
    descriptions = [' '.join(i.find_next('p').text.split()) for i in soup.find('div', id="description")]
    characteristics = [i.find_next('span', class_="param_name") for i in soup.find('div', id="characteristics")]

    images = [i['href'] for i in soup.find_all('a', class_="goods_gallery cboxElement")]
    try:
        os.mkdir(f'Aurora_ru/{articles[0]}')
    except FileExistsError:
        pass
    for image in images:
        response = requests.get(url=image, stream=True)
        with open(f'Aurora_ru/{articles[0]}/{image.split("/")[-1]}', 'wb') as f:
            f.write(response.content)

#    for name, article, price, description, characteristic, link1 in zip(names, articles, prices, descriptions, characteristics, links):
    flatten = names[0], articles[0], prices[0], descriptions[0], characteristics[0], link

    file = open(file_name, 'a', encoding='utf-8', newline='')
    writer = csv.writer(file, delimiter=';')
    writer.writerow(flatten)
    file.close()
    time.sleep(0.5)


print('Файл создан')

