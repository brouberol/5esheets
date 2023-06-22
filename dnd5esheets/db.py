from pathlib import Path
from typing import Generator
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine


db_dir = Path(__file__).parent / "db"
db_file = db_dir / "5esheets.db"
async_db_uri = f"sqlite+aiosqlite:///{db_file}"
db_uri = f"sqlite:///{db_file}"

async_engine = create_async_engine(
    async_db_uri,
    connect_args={"check_same_thread": False},  # only for sqlite
)

engine = create_engine(
    db_uri,
    connect_args={"check_same_thread": False},  # only for sqlite
)

async_session_factory = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_scoped_session() -> Generator[AsyncSession, None, None]:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()


@contextmanager
def create_session() -> Session:
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
