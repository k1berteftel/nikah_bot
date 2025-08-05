import datetime

from sqlalchemy import BigInteger, VARCHAR, ForeignKey, DateTime, Boolean, Column, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UsersTable(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    username: Mapped[str] = mapped_column(VARCHAR)
    name: Mapped[str] = mapped_column(VARCHAR)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    active: Mapped[int] = mapped_column(Integer, default=1)
    activity: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())
    entry: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=func.now())


class ChannelsSubTable(Base):
    __tablename__ = 'subs'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(VARCHAR)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    sub_end: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), default=None, nullable=True)


class AcceptChannelsTable(Base):
    __tablename__ = 'accept-channels'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    channel_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str | None] = mapped_column(VARCHAR, nullable=True)
    text: Mapped[str] = mapped_column(String)
    crossed: Mapped[int] = mapped_column(Integer, default=0)


class DiscountTable(Base):
    __tablename__ = 'discount'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    percent: Mapped[int] = mapped_column(Integer)


class DeeplinksTable(Base):
    __tablename__ = 'deeplinks'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    link: Mapped[str] = mapped_column(VARCHAR)
    entry: Mapped[int] = mapped_column(BigInteger, default=0)


class OpTable(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    chat_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(VARCHAR)
    link: Mapped[str] = mapped_column(VARCHAR)


class AdminsTable(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(VARCHAR)


class OneTimeLinksIdsTable(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    link: Mapped[str] = mapped_column(VARCHAR)


class StatisticsTable(Base):
    __tablename__ = 'statistics'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    buys_sum: Mapped[int] = mapped_column(Integer, default=0)
    today_buys: Mapped[int] = mapped_column(Integer, default=0)
    uploads_sum: Mapped[int] = mapped_column(Integer, default=0)
    today_uploads: Mapped[int] = mapped_column(Integer, default=0)

