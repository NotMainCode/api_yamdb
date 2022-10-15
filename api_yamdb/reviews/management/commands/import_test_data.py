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
        self.stdout.write("Test data loaded.")


def fill_table_from_csv(db, cursor, filename):
    """Clear table and fill data."""
    table = filename.split(".")[0]
    cursor.execute(f"DELETE FROM {table}")
    with open(
        os.path.join(settings.STATICFILES_DIRS_DATA, filename),
        "r",
        encoding="utf8",
    ) as csv_data:
        dr = csv.DictReader(csv_data, delimiter=";")
        for i in dr:
            keys = ",".join(i.keys())
            values = ",".join("'" + item + "'" for item in i.values())
            cursor.execute(f"INSERT INTO {table} ({keys}) VALUES ({values})")
    db.commit()


def fill_test_data():
    """Iterate for all tables, call funcs to prepare and fill data in db."""
    db = sqlite3.connect(os.path.join(settings.BASE_DIR, "db.sqlite3"))
    cursor = db.cursor()
    for filename in os.listdir(settings.STATICFILES_DIRS_DATA):
        fill_table_from_csv(db, cursor, filename)
