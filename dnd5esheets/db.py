from pathlib import Path
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
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

async_session_factory = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_scoped_session() -> AsyncGenerator[AsyncSession, None]:
    session = async_session_factory()
    try:
        yield session
    finally:
        await session.close()


class create_session:
    """Creates a new session to the database.

    This session creator looks like a function, and can be used in 2 ways:

    - as a context manager. The session will be committed if `commit_at_end=True`, and then closed.
    >>> with create_session(commit_at_end=True/False):
    ...     # code
    ... # session is now closed (and possibly committed if commit_at_end=True)

    - it can also be called directly
    >>> session = create_session()
    >>> # run things
    >>> session.commit()
    >>> session.close()

    The magic lies in having the create_session().__getattr__ method delegating calls to
    the underlying session object, as create_session() returns a create_session instance,
    not a Session instance, contrary to create_session().__enter__(), which returns a Session.

    """

    def __init__(self, commit_at_end: bool = False):
        self.session = session_factory()
        self.commit_at_end = commit_at_end

    def __enter__(self):
        return self.session

    def __exit__(self, *args, **kwargs):
        if self.commit_at_end:
            self.session.commit()
        self.session.close()

    def __getattr__(self, attr):
        return getattr(self.session, attr)
