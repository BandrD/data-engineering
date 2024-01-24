'''CREATE TABLE table1 (
    id          INTEGER,
    name        TEXT (256),
    price       REAL,
    quantity    INTEGER,
    category    TEXT (256),
    fromCity    TEXT (256),
    isAvailable TEXT (256),
    views       INTEGER
);'''

import json
import csv
import sqlite3

connection = sqlite3.connect('hw4base')
cursor = connection.cursor()

def insert_data_csv(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO table1 (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES( 
                 :name, :price, :quantity, :category, :fromCity, :isAvailable, :views
        )
    """, data)
    db.commit()

def read_csv(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        data_file = csv.DictReader(file, delimiter=';')
        data = []
        for row in data_file:
            if "category" not in row.keys() or row["category"] == "":
                row["category"] = None
            data.append(row)
    return data

data = read_csv("task_4_var_27_product_data.csv")
db = sqlite3.connect("hw4base")
insert_data_csv(db, data)

with open('task_4_var_27_update_data.text', 'r') as file:
    data = file.read()

def load_update_data(file_name):
    items = []
    with open(file_name, "r", encoding="utf-8") as f:
        lines = f.readlines()
        item = dict()
        for line in lines:
            if line == "=====\n":
                if item["method"] == "available":
                    item["param"] = item["param"] == "true"
                elif item["method"] != "remove":
                    item["param"] = float(item["param"])
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                splitted = line.split("::")
                item[splitted[0]] = splitted[1]

    return items

def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.executemany("DELETE FROM product WHERE name = ?", [name])
    db.commit()

def update_price_by_percent(db, name, percent):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET price = ROUND((price * (1 + ?)), 2) WHERE name = ?", [percent, name])
    cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
    db.commit()

def update_price(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET price = (price + ?) WHERE (name = ?) AND ((price + ?) > 0) ", [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()

def update_available(db, name, param):
    cursor = db.cursor()
    cursor.execute("UPDATE product SET isAvailable = ? WHERE (name = ?)", [param, name])
    cursor.execute("UPDATE product SET version = version + 1 where name = ?", [name])
    db.commit()

def update_quantity(db, name, value):
    cursor = db.cursor()
    res = cursor.execute("UPDATE product SET quantity = (quantity + ?) WHERE (name = ?) AND ((quantity + ?) > 0)", [value, name, value])
    if res.rowcount > 0:
        cursor.execute("UPDATE product SET version = version + 1 WHERE name = ?", [name])
        db.commit()

def handle_update(db, update_items):
    for item in update_items:
        match item["method"]:
            case "remove":
                print(f"deleting {item['name']}")
                delete_by_name(db, [item["name"]])
            case "price_percent":
                print(f"updating price {item['name']} {item['param']} %")
                update_price_by_percent(db, item["name"], item["param"])
            case "price_abs":
                print(f"updating price {item['name']} {item['param']}")
                update_price(db, item['name'], item['param'])
            case "available":
                print(f"updating available {item['name']} {item['param']}")
                update_available(db, item['name'], item['param'])
            case "quantity_add":
                print(f"updating quantity {item['name']} {item['param']}")
                update_quantity(db, item["name"], item["param"])
            case "quantity_sub":
                print(f"updating quantity {item['name']} {item['param']}")
                update_quantity(db, item["name"], item["param"])
            case _:
                print(f"unknown method {item['method']}")


def get_top_by_version(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM product ORDER BY version DESC LIMIT ?", [limit])
    items = list()

    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()

    return items


def get_stat_by_price(db):
    cursor = db.cursor()
    res = cursor.execute("""
        select category, count(*) as cnt, sum(price) as sum, avg(price) as avg, min(price) as min, max(price) as max from product
        group by category
    """)

    items = list()

    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()

    return items


def get_stat_by_quantity(db):
    cursor = db.cursor()
    res = cursor.execute("""
        select category, count(*) as cnt, sum(quantity) as sum, avg(quantity) as avg, min(quantity) as min, max(quantity) as max from product
        group by category
    """)

    items = list()

    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()

    return items


# Группировка по городам, в которых больше одного товара. Фильтр продуктов по просмотрам.
def query_for_city(db):
    cursor = db.cursor()
    res = cursor.execute("""
        select fromCity, count(*) as cnt from product
        where views > 2000
        group by fromCity
        having cnt > 1
    """)

    items = list()

    for row in res.fetchall():
        items.append(dict(row))
    cursor.close()

    return items

