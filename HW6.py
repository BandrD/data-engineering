from json2html import json2html
import requests
city_id = 1486209
appid = "85a4440bc2dc38c708baecf6fbd84d8a"
# Получение данных в формате JSON
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                   params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()

# Преобразование данных JSON в HTML-таблицу
html_table = json2html.convert(json=data)

# Вывод HTML-таблицы на экран
print(html_table)

with open('result.html', 'w', encoding='utf-8') as f:
    f.write(html_table)
