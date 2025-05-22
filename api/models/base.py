from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncAttrs

from api import util


class Base(AsyncAttrs, orm.DeclarativeBase):
    """
    Base model class that defines:
        id         - BIGINT, PRIMARY KEY
        created_at - TIMESTAMP WITHOUT TIMEZONE, NOT NULL, INDEX (sa properties: default=utcnow)
        updated_at - TIMESTAMP WITHOUT TIMEZONE, INDEX (sa properties: default=None, onupdate=utcnow)

    Usage example::

        class User(Base, table="service_users"):
            username: orm.Mapped[str]
    """

    def __init_subclass__(cls, **kwargs):
        if not hasattr(cls, "__tablename__") and "table" in kwargs:
            cls.__tablename__ = kwargs.pop("table")

        super().__init_subclass__(**kwargs)

    id: orm.Mapped[int] = orm.mapped_column(sa.BIGINT, primary_key=True, index=True)

    created_at: orm.Mapped[datetime] = orm.mapped_column(default=util.datetime.now, index=True)
    updated_at: orm.Mapped[datetime | None] = orm.mapped_column(
        default=None, onupdate=util.datetime.now, index=True
    )
