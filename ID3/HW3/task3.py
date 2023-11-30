from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import numpy as np

def handle_file(file_name):
    items = list()
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row


        star = BeautifulSoup(text, 'xml').star
        # print(star)

        item = dict()
        for el in star.contents:
            if el.name is not None:
                item[el.name] = el.get_text().strip()
    return item

items = []
for i in range(1, 500):
    file_name = f"zip_var_27_3/{i}.xml"
    result = handle_file(file_name)
    items.append(result)

items = sorted(items, key=lambda x: float(x['distance'].replace(' million km', '').strip()), reverse=True)

with open('result_filtered_distance.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(items, ensure_ascii=False))


filtered_items = []
for constellation in items:
    if constellation['constellation'] == 'Водолей':
        filtered_items.append(constellation)

with open('result_filtered_constellation.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

math_radius = list()
for item in items:
    math_radius.append(int(item['radius']))
    result_num = {}

    result_num['max'] = str(np.max(math_radius))
    result_num['min'] = str(np.min(math_radius))
    result_num['avg'] = str(np.average(math_radius))
    result_num['sum'] = str(np.sum(math_radius))
    result_num['std'] = str(np.std(math_radius))

    result_text = {}

    for item in items:
        elem = item.get('constellation')
        if (elem != None):
            if (elem in result_text):
                result_text[elem] += 1
            else:
                result_text[elem] = 1

    result_num['text'] = result_text
    with open('result_math_radius.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result_num, ensure_ascii=False))

handle_file("zip_var_27_3/27.xml")
