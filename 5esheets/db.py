from pathlib import Path

from peewee import SqliteDatabase

db_file = Path(__file__).parent / "db" / "5esheets.db"
db = SqliteDatabase(db_file)
