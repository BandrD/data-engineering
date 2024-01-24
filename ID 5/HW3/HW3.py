import json
import msgpack

from pymongo import MongoClient


def connect():
    client = MongoClient()
    db = client["test-database3"]
    return db.person

def get_msg():
    with open('task_3_item.msgpack', 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
    return data

def insert_many(collection):
    # Добавление записей в коллекцию
    collection.insert_many(get_msg())

def delete_by_salary(collection):
    res = collection.delete_many({
        "$or": [
            {"salary": {"$lt": 25_000}},
            {"salary": {"$gt": 175_000}},
        ]
    })
    print(res)

def update_age(collection):
    res = collection.update_many({}, {"$inc": {"age": 1}})
    print(res)

def increase_salary_by_job(collection):
    res = collection.update_many({
        "job": {"$in": ["Повар", "Учитель", "Бухгалтер"]}}, {
        "$mul": {"salary": 1.05}})
    print(res)

def increase_salary_by_city(collection):
    res = collection.update_many({
        "city": {"$in": ["Ереван", "Махадаонда", "Тбилиси"]}}, {
        "$mul": {"salary": 1.07}})
    print(res)

def increase_salary_hard(collection):
    res = collection.update_many({
        "$and": [{"city": {"$in": ["Ереван", "Москва", "Тбилиси"]}},
                {"job": {"$in": ["Программист", "IT-специалист", "Инженер"]}},
                {"age": {"$gt": 50}}]}, {
        "$mul": {"salary": 1.1}})
    print(res)

def delete_by_city_and_job(collection):
    res = collection.delete_many({
        "$and": [
            {"city": {"$in": ["Ташкент"]}},
            {"job": {"$in": ["Косметолог", "IT-специалист", "Бухгалтер"]}},
        ]
    })
    print(res)


print(get_msg())

insert_many(connect())
delete_by_salary(connect())
update_age(connect())
increase_salary_by_job(connect())
increase_salary_by_city(connect())
increase_salary_hard(connect())
delete_by_city_and_job(connect())