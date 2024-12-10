import contextlib
from typing import Optional


from pydantic import EmailStr
from sqlalchemy import select

from core.config import settings
from db.session import get_async_session


from models.class_ import Class
from models.user import Status

get_async_session_context = contextlib.asynccontextmanager(get_async_session)



async def create_base_db(

):

    async with get_async_session_context() as session:
        ...



async def start_db():
    await create_base_db()

