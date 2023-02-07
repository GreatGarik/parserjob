import requests
from bs4 import BeautifulSoup
import csv
import os
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
          'Accept': 'ext/html,application/xhtml+txml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}


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

links = ['/catalog/goods/Nitki-shveynie-Cotton--503-Aurora/1099/']
file = open(file_name, 'a', encoding='utf-8', newline='')
for link in links:
    link = f'https://aurora.ru{link}'
    response = requests.get(url=link, headers=header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    name = soup.find('h1', class_="goods_h1_name").text.strip()
    article = soup.find('div', class_="goods_artikul").text.split(':')[1].strip() if soup.find('div', class_="goods_artikul") and len(soup.find('div', class_="goods_artikul").text.split(':')) > 1 else f'Нет артикула {name}'.replace('/', '-')
    price = soup.find('span', class_="price").text.split()[0].strip() if soup.find('span', class_="price") else 'Нет цены'
    description = soup.find('div', id="description").text.strip()
    characteristics_names = [i.text for i in soup.find_all('span', class_="param_name")]
    characteristics_values = [i.text for i in soup.find_all('td', class_="param_val")]
    characteristics = [f'{k}: {v}' for k, v in zip(characteristics_names, characteristics_values)]



    if not os.path.exists(f'Aurora_ru/{article}'):
        images = [i['href'] for i in soup.find_all('a', class_="goods_gallery cboxElement")]
        os.mkdir(f'Aurora_ru/{article}')
        for image in images:
            response = requests.get(url=image, stream=True)
            with open(f'Aurora_ru/{article}/{image.split("/")[-1]}', 'wb') as f:
                f.write(response.content)

#    for name, article, price, description, characteristic, link1 in zip(names, articles, prices, descriptions, characteristics, links):
    flatten = name, article, price, description, ', '.join(characteristics), link
    writer = csv.writer(file, delimiter=';')
    writer.writerow(flatten)
    time.sleep(0.5)


file.close()

print('Файл создан')

