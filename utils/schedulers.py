import asyncio
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram_dialog import DialogManager
from aiogram.types import InlineKeyboardMarkup, Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database.action_data_class import DataInteraction
from data.channels_data import chats_title
from keyboards.keyboard import get_extend_keyboard


async def send_messages(bot: Bot, session: DataInteraction, keyboard: InlineKeyboardMarkup|None, message: Message, **kwargs):
    users = await session.get_users()
    text = kwargs.get('text')
    caption = kwargs.get('caption')
    photo = kwargs.get('photo')
    video = kwargs.get('video')
    if text:
        for user in users:
            try:
                await bot.send_message(
                    chat_id=user.user_id,
                    text=text.format(name=user.name),
                    reply_markup=keyboard
                )
                if user.active == 0:
                    await session.set_active(user.user_id, 1)
            except Exception as err:
                print(err)
                await session.set_active(user.user_id, 0)
    elif caption:
        if photo:
            for user in users:
                try:
                    await bot.send_photo(
                        chat_id=user.user_id,
                        photo=photo,
                        caption=caption.format(name=user.name),
                        reply_markup=keyboard
                    )
                    if user.active == 0:
                        await session.set_active(user.user_id, 1)
                except Exception as err:
                    print(err)
                    await session.set_active(user.user_id, 0)
        else:
            for user in users:
                try:
                    await bot.send_video(
                        chat_id=user.user_id,
                        video=video,
                        caption=caption.format(name=user.name),
                        reply_markup=keyboard
                    )
                    if user.active == 0:
                        await session.set_active(user.user_id, 1)
                except Exception as err:
                    print(err)
                    await session.set_active(user.user_id, 0)


async def check_sub(user_id: int, bot: Bot, scheduler: AsyncIOScheduler, session: DataInteraction):
    channels = await session.get_user_channels(user_id)
    for channel in channels:
        dif = (channel.sub_end - datetime.now()).days
        text = ''
        if dif == 5:
            text = f'До окончания периода подписки на канал "{channel.title}" осталось 5 дней'
        if dif == 1:
            text = (f'До окончания периода подписки на канал "{channel.title}" остался 1 день\n'
                    f'По истечению периода подписки вы будете удаленны с канала')
        if dif <= 0:
            text = 'К сожалению ваша подписка подошла к концу, вы будете удаленны из приватного канала'
            await bot.ban_chat_member(channel.channel_id, user_id)
            await bot.unban_chat_member(channel.channel_id, user_id)
            job_id = f'check_sub_{user_id}'
            job = scheduler.get_job(job_id=job_id)
            if job:
                job.remove()
        if text:
            await bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=get_extend_keyboard()
            )


async def update_today_statistics(session: DataInteraction, scheduler: AsyncIOScheduler):
    statistics = await session.get_statistics()
    await session.update_statistics('today_buys', -statistics.today_buys)
    await session.update_statistics('today_uploads', -statistics.today_uploads)
    start_date = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    scheduler.add_job(
        update_today_statistics,
        args=[session, scheduler],
        next_run_time=start_date
    )

