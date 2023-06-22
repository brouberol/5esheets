from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

db_dir = Path(__file__).parent / "db"
db_file = db_dir / "5esheets.db"
db_uri = f"sqlite:///{db_file}"
engine = create_engine(
    db_uri,
    connect_args={"check_same_thread": False},  # only for sqlite
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_scoped_session() -> Generator[Session, None, None]:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def create_session() -> Session:
    return next(create_scoped_session())
