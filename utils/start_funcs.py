from datetime import datetime, timedelta
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.action_data_class import DataInteraction
from keyboards.keyboard import get_extend_keyboard
from utils.schedulers import check_sub, update_today_statistics


async def stars_schedulers(bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler):
    for channel in await session.get_channels():
        dif = (channel.sub_end - datetime.now()).days
        user_id = channel.user_id
        if dif <= 0:
            await bot.ban_chat_member(channel.channel_id, user_id)
            await bot.unban_chat_member(channel.channel_id, user_id)
            await bot.send_message(
                chat_id=user_id,
                text='К сожалению ваша подписка подошла к концу, вы будете удаленны из приватного канала',
                reply_markup=get_extend_keyboard()
            )
            continue
        job_id = f'check_sub_{user_id}'
        job = scheduler.get_job(job_id=job_id)
        if not job:
            scheduler.add_job(
                check_sub,
                'interval',
                args=[user_id, bot, scheduler, session],
                id=job_id,
                days=1
            )
    start_date = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    scheduler.add_job(
        update_today_statistics,
        args=[session, scheduler],
        next_run_time=start_date
    )

