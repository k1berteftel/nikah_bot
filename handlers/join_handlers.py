from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.types import ChatJoinRequest

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.action_data_class import DataInteraction


join_router = Router()


@join_router.chat_join_request()
async def apply_join_request(request: ChatJoinRequest, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler):
    chat_id = request.chat.id
    if chat_id in [channel.channel_id for channel in await session.get_accept_channels()]:
        accept_channel = await session.get_accept_channel(chat_id)
        await session.update_accept_crossed(chat_id)
        await request.answer(accept_channel.text)
        await request.approve()
    else:
        try:
            user = await session.get_user(request.from_user.id)
            if not user.sub_end or user.sub_end < datetime.now():
                await request.decline()
                return
            await request.approve()
        except Exception as err:
            print(err)
    await request.decline()
