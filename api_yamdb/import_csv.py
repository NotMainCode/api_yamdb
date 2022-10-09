import sqlite3
import csv

db = sqlite3.connect("db.sqlite3")
cursor = db.cursor()

def FillCategories():
    cursor.execute("DELETE FROM reviews_categories")
    with open('static/data/category.csv', 'r', encoding='utf8') as category_data:
        dr = csv.DictReader(category_data, delimiter=',')
        to_db = [(i['id'], i['name'], i['slug']) for i in dr]
    cursor.executemany("INSERT INTO reviews_categories VALUES (?,?,?);", to_db)
    db.commit()

def FillGenres():
    cursor.execute("DELETE FROM reviews_genres")
    with open('static/data/genre.csv', 'r', encoding='utf8') as genre_data:
        dr = csv.DictReader(genre_data, delimiter=',')
        to_db = [(i['id'], i['name'], i['slug']) for i in dr]
    cursor.executemany("INSERT INTO reviews_genres VALUES (?,?,?);", to_db)
    db.commit()

def FillTitles():
    cursor.execute("DELETE FROM reviews_title")
    with open('static/data/titles.csv', 'r', encoding='utf8') as title_data:
        dr = csv.DictReader(title_data, delimiter=';')
        to_db = [(i['id'], i['name'], i['year'], i['name'], i['category']) for i in dr]
    cursor.executemany("INSERT INTO reviews_title VALUES (?,?,?,?,?);", to_db)
    db.commit()

def FillGenreTitles():
    cursor.execute("DELETE FROM reviews_title_genre")
    with open('static/data/genre_title.csv', 'r', encoding='utf8') as genre_titles_data:
        dr = csv.DictReader(genre_titles_data, delimiter=',')
        to_db = [(i['id'], i['title_id'], i['genre_id']) for i in dr]
    cursor.executemany("INSERT INTO reviews_title_genre VALUES (?,?,?);", to_db)
    db.commit()

def FillReview():
    cursor.execute("DELETE FROM reviews_review")
    with open('static/data/review.csv', 'r', encoding='utf8') as review_data:
        dr = csv.DictReader(review_data, delimiter=';')
        to_db = [(i['id'], i['text'], i['score'], i['pub_date'], i['author'], i['title_id']) for i in dr]
    cursor.executemany("INSERT INTO reviews_review VALUES (?,?,?,?,?,?);", to_db)
    db.commit()


def FillComments():
    cursor.execute("DELETE FROM reviews_comment")
    with open('static/data/comments.csv', 'r', encoding='utf8') as comments_data:
        dr = csv.DictReader(comments_data, delimiter=';')
        to_db = [(i['id'], i['text'], i['pub_date'], i['author'], i['review_id']) for i in dr]
    cursor.executemany("INSERT INTO reviews_comment VALUES (?,?,?,?,?);", to_db)
    db.commit()

def FillUsers():
    cursor.execute("DELETE FROM users_user WHERE username !='admin'")
    with open('static/data/users.csv', 'r', encoding='utf8') as users_data:
        dr = csv.DictReader(users_data, delimiter=',')
        to_db = [(i['id'], '', '', '', i['username'],  i['last_name'], '', True, '',  i['email'], i['first_name'], i['bio'], '', i['role']) for i in dr]
    cursor.executemany("INSERT INTO users_user VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);", to_db)
    db.commit()

FillCategories()
FillGenres()
FillTitles()
FillGenreTitles()
FillReview()
FillComments()
FillUsers()

