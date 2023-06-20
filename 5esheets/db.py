from pathlib import Path

from peewee import SqliteDatabase

db_dir = Path(__file__).parent / "db"
db_file = db_dir / "5esheets.db"
db = SqliteDatabase(db_file)
