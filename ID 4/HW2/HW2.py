'''
CREATE TABLE tabl2 (
    id    INTEGER    PRIMARY KEY,
    title TEXT (256),
    price INTEGER,
    place TEXT (256),
    date  TEXT (256)
);
'''

import os
import json
import sqlite3

connection = sqlite3.connect('first')
cursor = connection.cursor()

result = cursor.execute("SELECT * FROM tabl2")
print(result.fetchall())

def parse_data(file_name):
    with open(file_name, "rb") as file:
        data_file = json.load(file)
    return data_file

def connect_to_db(file_name):
    return sqlite3.connect("first")

def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO tabl2 (title, price, place, date)
        VALUES( 
                :title, :price, :place, :date
        )
    """, data)
    db.commit()

items = parse_data("task_2_var_27_subitem.json")
db = connect_to_db("first")
insert_data(db, items)

def statistical_characteristics(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        MIN(price) as min,
        MAX(price) as max,
        AVG(price) as avg,
        SUM(price) as sum
        FROM tabl2
        JOIN title ON tabl2.price = title.views
    """)

    items_st = []
    res = res.fetchone()
    items_st.append(res)
    cursor.close()

    return items_st

st = statistical_characteristics(db)

with open('r_statistical.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(st, ensure_ascii=False))


def reiterative(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT title.title
        FROM title
        JOIN tabl2 ON title.title = tabl2.title
    """)

    items_list = []
    res = res.fetchall()
    items_list.append(res)
    cursor.close()

    return items_list

rt = reiterative(db)

with open('rt.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(rt, ensure_ascii=False))

def common_list(db):
    cursor = db.cursor()

    res = cursor.execute("""
            SELECT DISTINCT title.title
            FROM title
            JOIN tabl2 ON title.title = tabl2.title
        """)

    items_list_full = []
    for row in res:
        items_list_full.append(row[0])

    cursor.close()

    return items_list_full

cl = common_list(db)

with open('cl.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(cl, ensure_ascii=False))