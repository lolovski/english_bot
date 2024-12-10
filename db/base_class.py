from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):

    id = mapped_column(Integer, primary_key=True, autoincrement=True)