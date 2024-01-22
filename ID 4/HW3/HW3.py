'''
CREATE TABLE table1 (
    id           INTEGER    PRIMARY KEY,
    artist       TEXT (256),
    song         TEXT (256),
    duration_ms  INTEGER,
    year         INTEGER,
    tempo        INTEGER,
    genre        TEXT (256),
    acousticness REAL,
    energy       REAL,
    key          INTEGER,
    popularity   INTEGER,
    loudness     REAL
);
'''
import json
import csv
import pickle
import sqlite3

with open('task_3_var_27_part_2.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)

connection = sqlite3.connect('hw3base')
cursor = connection.cursor()


def parse_data(file_name):
    with open(file_name, "rb") as file:
        data_file = pickle.load(file)
    return data_file

def connect_to_db(file_name):
    return sqlite3.connect("hw3base")

def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO table1 (artist, song, duration_ms, year, tempo, genre, acousticness, energy, popularity)
        VALUES( 
                :artist, :song, :duration_ms, :year, :tempo, :genre, :acousticness, :energy, :popularity
        )
    """, data)
    db.commit()

items = parse_data("task_3_var_27_part_2.pkl")
db = connect_to_db("hw3base")
insert_data(db, items)


def insert_data_csv(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO table1 (artist, song, duration_ms, year, tempo, genre, energy, key, loudness)
        VALUES( 
                :artist, :song, :duration_ms, :year, :tempo, :genre, :energy, :key, :loudness
        )
    """, data)
    db.commit()

def read_csv(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        data_file = csv.DictReader(file, delimiter=';')
        data = []
        for row in data_file:
            data.append(row)
    return data

data = read_csv("task_3_var_27_part_1.csv")
db = sqlite3.connect("hw3base")
insert_data_csv(db, data)


def get_top_by_year(db):
    cursor = db.cursor()

    res = cursor.execute(
        "SELECT * FROM table1 ORDER BY year LIMIT 37")
    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(row)
    cursor.close()

    return items_list

gt = get_top_by_year(db)

with open('gt.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(gt, ensure_ascii=False))


def statistical_characteristics(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        MIN(duration_ms) as min,
        MAX(duration_ms) as max,
        AVG(duration_ms) as avg,
        SUM(duration_ms) as sum
        FROM table1
    """)

    items_st = []
    res = res.fetchone()
    items_st.append(res)
    cursor.close()

    return items_st

st = statistical_characteristics(db)

with open('r_statistical.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(st, ensure_ascii=False))


def frequency(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT genre, COUNT(*) AS frequency FROM table1 GROUP BY genre;
    """)

    items_fr = []
    res = res.fetchall()
    items_fr.append(res)
    cursor.close()

    return items_fr

fr = frequency(db)

with open('fr.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(fr, ensure_ascii=False))


def predicate(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT * 
        FROM table1 
        WHERE tempo >= 150
        ORDER BY year DESC LIMIT 42;
    """)

    items_pr = []
    res = res.fetchall()
    items_pr.append(res)
    cursor.close()

    return items_pr

pr = predicate(db)

with open('pr.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(pr, ensure_ascii=False))



