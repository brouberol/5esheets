from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from dnd5esheets.db import create_scoped_session

debug_api = APIRouter(prefix="/debug", include_in_schema=False)


@debug_api.get("/sqlite-version")
async def sqlite_version(
    session: AsyncSession = Depends(create_scoped_session),
):
    result = await session.execute(text("select sqlite_version()"))
    version = result.scalar_one()
    return {"version": version}
