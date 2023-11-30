from bs4 import BeautifulSoup
import re
import json
import numpy as np
from collections import Counter

def handle_file(file_name):
    items=list()
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        root = BeautifulSoup(text, 'xml')
        for clothing in root.find_all("clothing"):
            item=dict()
            for el in clothing.contents:
                if el.name is None:
                    continue
                elif el.name=="price" or el.name=="reviews":
                    item[el.name]=int(el.get_text().strip())
                elif el.name=="price" or el.name=="rating":
                    item[el.name]=float(el.get_text().strip())
                elif el.name=="new":
                    item[el.name]=el.get_text().strip()=="+"
                elif el.name=="exclusive" or el.name=="sporty":
                    item[el.name]=el.get_text().strip()=="yes"
                else:
                    item[el.name]=el.get_text().strip()
            items.append(item)
    return items


items=[]
for i in range(1,100):
    file_name=f"zip_var_27_4/{i}.xml"
    items+=handle_file(file_name)

items=sorted(items, key=lambda x: x['price'], reverse=True)

with open("results_price.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items,ensure_ascii=False))

filtered_items=[]
for root in items:
    if root['reviews']>=950000:
        filtered_items.append(root)

with open("results_reviews.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items,ensure_ascii=False))

reviews = list()

for item in items:
    reviews.append(int(item['reviews']))

result_num = {}

result_num['max'] = str(np.max(reviews))
result_num['min'] = str(np.min(reviews))
result_num['avg'] = str(np.average(reviews))
result_num['sum'] = str(np.sum(reviews))
result_num['std'] = str(np.std(reviews))

result_text = {}

for item in items:
    elem = item.get('category')
    if(elem != None):
        if(elem in result_text):
            result_text[elem] += 1
        else:
            result_text[elem] = 1


    result_num['text'] = result_text

with open("results_math.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(result_num, ensure_ascii=False))
