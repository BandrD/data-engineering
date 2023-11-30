from bs4 import BeautifulSoup
import re
import json
import numpy as np

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        # print(site)

        item = dict()
        item['type'] = site.find_all("span", string=re.compile("Тип:"))[0].get_text().replace("Тип:", "").strip()
        item['title'] = site.find_all("h1", string=re.compile("Турнир:"))[0].get_text().replace("Турнир:", "").strip()
        address = site.find_all('p', attrs={'class': 'address-p'})[0].get_text().split('Начало')

        item['city'] = address[0].replace('Город:', '').strip()
        item['date'] = address[1].strip()
        item['count'] = int(site.find_all('span', attrs={'class': 'count'})[0].get_text().split(':')[1].strip())
        item['count'] = int(site.find_all('span', attrs={'class': 'year'})[0].get_text().split(':')[1].replace('мин', '').strip())
        item['minRating'] = int(site.find_all("span", string=re.compile("Минимальный рейтинг для участия:"))[0].get_text().split(':')[1].strip())
        item['img'] = site.find_all('img')[0]['src']
        item['views'] = int(site.find_all("span", string=re.compile("Просмотры:"))[0].get_text().split(':')[1].strip())
        item['rating'] = float(site.find_all("span", string=re.compile("Рейтинг:"))[0].get_text().split(':')[1].strip())

        # print(item['type'])
        # print(item['title'])
        # print(item['city'])
        # print(item['date'][2:7])
        # print(item['minRating'])
        # print(item['img'])
        # print(item['views'])
        # print(item['rating'])

        return item
items = []
for i in range(1,999):
    file_name = f'zip_var_27/{i}.html'
    result = handle_file(file_name)
    items.append(result)

items = sorted(items, key=lambda x: x['views'], reverse=True)

with open('results_all_1.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items))

# Фильтрация по минимальнмоу рейтингу и запись в отдельный файл
filtered_items = []
for tournament in items:
    if tournament['minRating'] >= 2500:
        filtered_items.append(tournament)

with open('filtered_results_all_1.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_items))

#статистические характеристики (сумма, мин/макс, среднее и т.д.)

views = list()

for item in items:
    views.append(int(item['views']))

result_num = {}

result_num['max'] = str(np.max(views))
result_num['min'] = str(np.min(views))
result_num['avg'] = str(np.average(views))
result_num['sum'] = str(np.sum(views))
result_num['std'] = str(np.std(views))

print(result_num)

result_text = {}

for item in items:
    elements = item['type']
    if(elements in result_text):
        result_text[elements] += 1
    else:
        result_text[elements] = 1

result_num['text'] = result_text
with open('stat.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(result_num))


# print(len(items))
# print(len(filtered_items))



handle_file("zip_var_27/27.html")
