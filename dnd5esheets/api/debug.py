from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session

debug_api = APIRouter(prefix="/debug", include_in_schema=False)


@debug_api.get("/sqlite")
async def sqlite_version(
    session: AsyncSession = Depends(create_scoped_session),
):
    """Return debug information about the sqlite database"""
    version = (await session.execute(text("select sqlite_version()"))).scalar_one()

    # Taken from https://til.simonwillison.net/sqlite/python-sqlite-environment
    pragma_compile_options = (await session.execute(text("pragma compile_options"))).scalars().all()
    pragmas = {}
    for pragma in (
        "foreign_keys",
        "defer_foreign_keys",
        "ignore_check_constraints",
        "legacy_alter_table",
        "recursive_triggers",
        "writable_schema",
    ):
        pragmas[pragma] = (await session.execute(text(f"pragma {pragma}"))).scalar()
    return {
        "version": version,
        "compile_options": pragma_compile_options,
        "pragmas": pragmas,
    }
