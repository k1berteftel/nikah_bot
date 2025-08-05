import calendar
import datetime

from sqlalchemy import select, insert, update, column, text, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from database.model import (UsersTable, DeeplinksTable, OneTimeLinksIdsTable, AdminsTable, OpTable, ChannelsSubTable,
                            StatisticsTable, DiscountTable, AcceptChannelsTable)


async def configurate_tables(sessions: async_sessionmaker):
    async with sessions() as session:
        result = await session.scalar(select(StatisticsTable))
        if result:
            return
        await session.execute(insert(StatisticsTable))
        await session.commit()


class DataInteraction():
    def __init__(self, session: async_sessionmaker):
        self._sessions = session

    async def check_user(self, user_id: int) -> bool:
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.user_id == user_id))
        return True if result else False

    async def add_user(self, user_id: int, username: str, name: str):
        if await self.check_user(user_id):
            return
        async with self._sessions() as session:
            await session.execute(insert(UsersTable).values(
                user_id=user_id,
                username=username,
                name=name,
            ))
            await session.commit()

    async def add_op(self, chat_id: int, name: str, link: str):
        async with self._sessions() as session:
            await session.execute(insert(OpTable).values(
                chat_id=chat_id,
                name=name,
                link=link
            ))
            await session.commit()

    async def add_entry(self, link: str):
        async with self._sessions() as session:
            await session.execute(update(DeeplinksTable).where(DeeplinksTable.link == link).values(
                entry=DeeplinksTable.entry+1
            ))
            await session.commit()

    async def add_deeplink(self, link: str):
        async with self._sessions() as session:
            await session.execute(insert(DeeplinksTable).values(
                link=link
            ))
            await session.commit()

    async def add_link(self, link: str):
        async with self._sessions() as session:
            await session.execute(insert(OneTimeLinksIdsTable).values(
                link=link
            ))
            await session.commit()

    async def add_admin(self, user_id: int, name: str):
        async with self._sessions() as session:
            await session.execute(insert(AdminsTable).values(
                user_id=user_id,
                name=name
            ))
            await session.commit()

    async def add_channel(self, user_id: int, channel_id: int, title: str):
        async with self._sessions() as session:
            today = datetime.datetime.now()
            days = calendar.monthrange(today.year, today.month)[1]
            new_date = today + datetime.timedelta(days=days)
            sub_end = new_date
            await session.execute(insert(ChannelsSubTable).values(
                user_id=user_id,
                title=title,
                channel_id=channel_id,
                sub_end=sub_end
            ))
            await session.commit()

    async def add_accept_channel(self, channel_id: int, title: str, text: str):
        async with self._sessions() as session:
            await session.execute(insert(AcceptChannelsTable).values(
                channel_id=channel_id,
                name=title,
                text=text
            ))
            await session.commit()

    async def add_discount(self, percent: int):
        async with self._sessions() as session:
            await session.execute(insert(DiscountTable).values(percent=percent))
            await session.commit()

    async def get_discount(self):
        async with self._sessions() as session:
            result = await session.scalar(select(DiscountTable))
        return result

    async def get_statistics(self):
        async with self._sessions() as session:
            result = await session.scalar(select(StatisticsTable))
        return result

    async def get_accept_channels(self):
        async with self._sessions() as session:
            result = await session.scalars(select(AcceptChannelsTable))
        return result.fetchall()

    async def get_accept_channel(self, channel_id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(AcceptChannelsTable).where(
                AcceptChannelsTable.channel_id == channel_id
            ))
        return result

    async def get_users(self):
        async with self._sessions() as session:
            result = await session.scalars(select(UsersTable))
        return result.fetchall()

    async def get_user(self, user_id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.user_id == user_id))
        return result

    async def get_user_by_username(self, username: str):
        async with self._sessions() as session:
            result = await session.scalar(select(UsersTable).where(UsersTable.username == username))
        return result

    async def get_user_channels(self, user_id: int):
        async with self._sessions() as session:
            result = await session.scalars(select(ChannelsSubTable).where(ChannelsSubTable.user_id == user_id))
        return result.fetchall()

    async def get_user_channel(self, user_id: int, channel_id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(ChannelsSubTable).where(
                and_(
                    ChannelsSubTable.user_id == user_id,
                    ChannelsSubTable.channel_id == channel_id
                )
            ))
        return result

    async def get_channels(self):
        async with self._sessions() as session:
            result = await session.scalars(select(ChannelsSubTable))
        return result.fetchall()

    async def get_op(self):
        async with self._sessions() as session:
            result = await session.scalars(select(OpTable))
        return result.fetchall()

    async def get_op_by_chat_id(self, chat_id: int):
        async with self._sessions() as session:
            result = await session.scalar(select(OpTable).where(OpTable.chat_id == chat_id))
        return result

    async def get_links(self):
        async with self._sessions() as session:
            result = await session.scalars(select(OneTimeLinksIdsTable))
        return result.fetchall()

    async def get_admins(self):
        async with self._sessions() as session:
            result = await session.scalars(select(AdminsTable))
        return result.fetchall()

    async def get_deeplinks(self):
        async with self._sessions() as session:
            result = await session.scalars(select(DeeplinksTable))
        return result.fetchall()

    async def update_channel_sub(self, user_id: int, channel_id: int):
        async with self._sessions() as session:
            async with self._sessions() as session:
                channel = await session.scalar(select(ChannelsSubTable).where(
                    and_(
                        ChannelsSubTable.channel_id == channel_id,
                        ChannelsSubTable.user_id == user_id
                    )
                ))
                if not channel:
                    date = channel.sub_end
                    days = calendar.monthrange(date.year, date.month)[1]
                    new_date = date + datetime.timedelta(days=days)
                    channel.sub_end = new_date
                await session.commit()

    async def update_statistics(self, column: str, amount: int):
        stmt = update(StatisticsTable).values({
            column: getattr(StatisticsTable, column) + amount
        })
        async with self._sessions() as session:
            await session.execute(stmt)
            await session.commit()

    async def update_accept_crossed(self, channel_id: int):
        async with self._sessions() as session:
            await session.execute(update(AcceptChannelsTable).where(
                AcceptChannelsTable.channel_id == channel_id
            ).values(
                crossed=AcceptChannelsTable.crossed + 1
            ))
            await session.commit()

    async def set_activity(self, user_id: int):
        async with self._sessions() as session:
            await session.execute(update(UsersTable).where(UsersTable.user_id == user_id).values(
                activity=datetime.datetime.today()
            ))
            await session.commit()

    async def set_accept_channel_text(self, channel_id: int, text: str):
        async with self._sessions() as session:
            await session.execute(update(AcceptChannelsTable).where(
                AcceptChannelsTable.channel_id == channel_id
            ).values(
                text=text
            ))
            await session.commit()

    async def set_active(self, user_id: int, active: int):
        async with self._sessions() as session:
            await session.execute(update(UsersTable).where(UsersTable.user_id == user_id).values(
                active=active
            ))
            await session.commit()

    async def set_button_link(self, chat_id: int, link: str):
        async with self._sessions() as session:
            await session.execute(update(OpTable).where(OpTable.chat_id == chat_id).values(
                link=link
            ))
            await session.commit()

    async def del_deeplink(self, link: str):
        async with self._sessions() as session:
            await session.execute(delete(DeeplinksTable).where(DeeplinksTable.link == link))
            await session.commit()

    async def del_link(self, link_id: str):
        async with self._sessions() as session:
            await session.execute(delete(OneTimeLinksIdsTable).where(OneTimeLinksIdsTable.link == link_id))
            await session.commit()

    async def del_admin(self, user_id: int):
        async with self._sessions() as session:
            await session.execute(delete(AdminsTable).where(AdminsTable.user_id == user_id))
            await session.commit()

    async def del_discount(self):
        async with self._sessions() as session:
            await session.execute(delete(DiscountTable))
            await session.commit()

    async def del_op_channel(self, chat_id: int):
        async with self._sessions() as session:
            await session.execute(delete(OpTable).where(OpTable.chat_id == chat_id))
            await session.commit()

    async def del_accept_channel(self, channel_id: int):
        async with self._sessions() as session:
            await session.execute(delete(AcceptChannelsTable).where(
                AcceptChannelsTable.channel_id == channel_id))
            await session.commit()