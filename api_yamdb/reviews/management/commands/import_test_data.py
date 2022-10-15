"""Import test data into db from /static/data/*.csv."""

import csv
import os.path
import sqlite3

from django.core.management.base import BaseCommand

from api_yamdb import settings


class Command(BaseCommand):
    """Import test data in database."""

    def handle(self, *args, **options):
        fill_test_data()
        self.stdout.write('Test data loaded.')


def fill_table(db, cursor, table, to_db):
    """Clear table and fill data."""
    cursor.execute(f"DELETE FROM {table}")
    fields = ",".join('?' * len(to_db[0]))
    cursor.executemany(f"INSERT INTO {table} VALUES ({fields});", to_db)
    db.commit()


def get_category_data_from_csv():
    """Prepare data to table reviews_category."""
    with open(os.path.join(settings.STATICFILES_DIRS_DATA, "category.csv"),
              "r", encoding="utf8") as category_data:
        dr = csv.DictReader(category_data, delimiter=";")
        to_db = [(i["id"], i["name"], i["slug"]) for i in dr]
    return to_db


def get_genre_data_from_csv():
    """Prepare data to table reviews_genre."""
    with open(os.path.join(settings.STATICFILES_DIRS_DATA, "genre.csv"),
              "r", encoding="utf8") as genre_data:
        dr = csv.DictReader(genre_data, delimiter=";")
        to_db = [(i["id"], i["name"], i["slug"]) for i in dr]
    return to_db


def get_title_data_from_csv():
    """Prepare data to table reviews_title."""
    with open(os.path.join(settings.STATICFILES_DIRS_DATA, "titles.csv"),
              "r", encoding="utf8") as title_data:
        dr = csv.DictReader(title_data, delimiter=";")
        to_db = [
            (i["id"], i["name"], i["year"], '', i["category"])
            for i in dr
        ]
    return to_db


def get_genre_title_data_from_csv():
    """Prepare data to table reviews_title_genre."""
    with open(os.path.join(settings.STATICFILES_DIRS_DATA, "genre_title.csv"),
              "r", encoding="utf8") as genre_titles_data:
        dr = csv.DictReader(genre_titles_data, delimiter=";")
        to_db = [(i["id"], i["title_id"], i["genre_id"]) for i in dr]
    return to_db


def get_review_data_from_csv():
    """Prepare data to table reviews_review."""
    with open(os.path.join(settings.STATICFILES_DIRS_DATA, "review.csv"),
              "r", encoding="utf8") as review_data:
        dr = csv.DictReader(review_data, delimiter=";")
        to_db = [
            (
                i["id"],
                i["text"],
                i["score"],
                i["pub_date"],
                i["author"],
                i["title_id"],
            )
            for i in dr
        ]
    return to_db


def get_comment_data_from_csv():
    """Prepare data to table reviews_comment."""
    with open(os.path.join(settings.STATICFILES_DIRS_DATA, "comments.csv"),
              "r", encoding="utf8") as comments_data:
        dr = csv.DictReader(comments_data, delimiter=";")
        to_db = [
            (i["id"], i["text"], i["pub_date"], i["author"], i["review_id"])
            for i in dr
        ]
    return to_db


def get_user_data_from_csv():
    """Prepare data to table users_user."""
    with open(os.path.join(settings.STATICFILES_DIRS_DATA, "users.csv"),
              "r", encoding="utf8") as users_data:
        dr = csv.DictReader(users_data, delimiter=";")
        to_db = [
            (
                i["id"],
                "",
                "",
                "",
                i["username"],
                i["first_name"],
                i["last_name"],
                "",
                True,
                "",
                i["role"],
                i["email"],
                i["bio"],
            )
            for i in dr
        ]
    return to_db


def fill_test_data():
    """Iterate for all tables, call funcs to prepare and fill data in db."""
    db = sqlite3.connect(os.path.join(settings.BASE_DIR, "db.sqlite3"))
    cursor = db.cursor()
    get_data_csv = {
        "reviews_category": get_category_data_from_csv,
        "reviews_genre": get_genre_data_from_csv,
        "reviews_title": get_title_data_from_csv,
        "reviews_title_genre": get_genre_title_data_from_csv,
        "reviews_review": get_review_data_from_csv,
        "reviews_comment": get_comment_data_from_csv,
        "users_user": get_user_data_from_csv
    }
    for table in get_data_csv:
        data = get_data_csv[table]()
        fill_table(db, cursor, table, data)
