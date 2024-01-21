import json
import pickle
import sqlite3

connection = sqlite3.connect('first')
cursor = connection.cursor()

result = cursor.execute("SELECT * FROM title")
print(result.fetchall())

def parse_data(file_name):
    with open(file_name, "rb") as file:
        data_file = pickle.load(file)
    return data_file

def connect_to_db(file_name):
    return sqlite3.connect("first")



def insert_data(db, data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO title (title, author, genre, pages, published_year, isbn, rating, views)
        VALUES( 
                :title, :author, :genre, :pages, :published_year, :isbn, :rating, :views
        )
    """, data)
    db.commit()

items = parse_data("task_1_var_27_item.pkl")
db = connect_to_db("first")
insert_data(db, items)



def get_top_by_title(db):
    cursor = db.cursor()

    res = cursor.execute(
        "SELECT * FROM title ORDER BY author DESC LIMIT 15")
    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(row)
    cursor.close()

    return items_list


def get_top_views(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT * 
        FROM title 
        WHERE views > 40000
        ORDER BY views DESC LIMIT 15
        """)

    res = res.fetchall()

    items_list = []

    for row in res:
        items_list.append(row)
    cursor.close()

    return items_list


def statistical_characteristics(db):
    cursor = db.cursor()

    res = cursor.execute("""
        SELECT 
        MIN(views) as min,
        MAX(views) as max,
        AVG(views) as avg,
        SUM(views) as sum
        FROM title
    """)

    items_st = []
    res = res.fetchone()
    items_st.append(res)
    cursor.close()

    return items_st


items = parse_data('task_1_var_27_item.pkl')


def tag_frequency(db):
    cursor = db.cursor()

    result_tag = cursor.execute("""
                    SELECT
                        CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM title) as count,
                        title
                    FROM title
                    GROUP BY title

    """)
    items_tag = []
    for row in result_tag.fetchall():
        items_tag.append(row)

    cursor.close()
    return items_tag


db = connect_to_db("first")

st = statistical_characteristics(db)
tag = tag_frequency(db)

res_1 = get_top_by_title(db)
res_2 = get_top_views(db)

with open('r_task1.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_1, ensure_ascii=False))

with open('r_task1_filter.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(res_2, ensure_ascii=False))

with open('r_statistical.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(st, ensure_ascii=False))

with open('r_tag.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(tag, ensure_ascii=False))