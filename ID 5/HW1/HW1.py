import json
from pymongo import MongoClient

#Функция подключения и создания БД в MongoDB:
def connect():
    client = MongoClient()
    db = client["test-database"]
    return db.person_data


def open_json(file_json):
    with open(file_json, "r", encoding="utf-8") as file:
        res = json.load(file)


    return res

#Загружаем данные в коллекцию(таблица с данными):
def insert_many(collection, data):
    collection.insert_many(data)


def sort_by_salary(collection):

    items = []
    for person in collection.find({}, limit=10).sort({"salary": -1}):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open("sort_salary.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))


def filter_age(collection):
    items = []
    for person in collection.find({"age": {"$lt" : 30}}, limit=15).sort({"salary": -1}):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open("filter_age.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))


def filter_city(collection):
    items = []
    for person in (collection.find({"city": "Краков", "job":{"$in" : ["IT-специалист", "Менеджер", "Водитель"]}}, limit=10)
            .sort({"age": 1})):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open("filter_city.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))


def filter_complex(collection):
    items = []
    for person in (collection.find({
        "age": {"$gt": 22, "$lt": 45},
        "year": {"$in": [2019, 2020, 2021, 2022]},
        "$or": [{"salary": {"$gt": 50000, "$lte": 75000}},
                {"salary": {"$gt": 125000, "$lt": 150000}}]
                                    })):
        person["_id"] = str(person["_id"])
        items.append(person)

    with open("filter_complex.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(items, ensure_ascii=False))



data = open_json("task_1_item.json")
# insert_many(connect(), data) #Коментируем запрос, как только загрузили данные в таблицу(коллекцию)

sort_by_salary(connect())
filter_age(connect())
filter_city(connect())
filter_complex(connect())