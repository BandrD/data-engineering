from bs4 import BeautifulSoup
import re
import json
import numpy as np

def handle_file(file_name):
    items = list()
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row


        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all('div', attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all('img')[0]['src']
            item['title'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace('₽', '').replace(' ', '').strip())
            item['bonus'] = int(product.strong.get_text().replace('+ начислим ', '').replace(' бонусов','').strip())
            props = product.ul.find_all('li')
            for prop in props:
                item[prop['type']] = prop.get_text().strip()
            items.append(item)

            # print(item)

    return items

items = []

for i in range(1, 45):
    file_name = f"zip_var_27_2/{i}.html"
    items += handle_file(file_name)

items = sorted(items, key=lambda x: x['id'], reverse=True)

with open('result_filtered_id.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items))


filt_items = list()
for item in items:
    if(item['bonus'] >= 4000):
        filt_items.append(item)


with open('result_filtered_bonus.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filt_items))




prices = list()

for item in items:
    prices.append(int(item['price']))

result_num = {}

result_num['max'] = str(np.max(prices))
result_num['min'] = str(np.min(prices))
result_num['avg'] = str(np.average(prices))
result_num['sum'] = str(np.sum(prices))
result_num['std'] = str(np.std(prices))

result_text = {}

for item in items:
    elem = item.get('matrix')
    if(elem != None):
        if(elem in result_text):
            result_text[elem] += 1
        else:
            result_text[elem] = 1

result_num['text'] = result_text
with open('result_math.json', 'w', encoding='utf-8') as f:
    json.dump(result_num, f, ensure_ascii=False)

handle_file("zip_var_27_2/27.html")
