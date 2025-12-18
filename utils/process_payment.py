from typing import Literal
import asyncio
from asyncio import TimeoutError

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.payments import check_oxa_payment
from database.action_data_class import DataInteraction
from utils.text_utils import get_form_text
from config_data.config import Config, load_config
from utils.schedulers import check_sub
from data.channels_data import chats, chats_title


config: Config = load_config()


async def wait_for_payment(
        payment_id: str,
        user_id: int,
        bot: Bot,
        session: DataInteraction,
        scheduler: AsyncIOScheduler,
        data: dict,
        payment_type: Literal['crypto'],
        timeout: int = 60 * 30,
        check_interval: int = 7
):
    """
    Ожидает оплаты в фоне. Завершается при оплате или по таймауту.
    """
    try:
        await asyncio.wait_for(_poll_payment(payment_id, user_id, bot, session, scheduler, data, payment_type, check_interval),
                               timeout=timeout)

    except TimeoutError:
        print(f"Платёж {payment_id} истёк (таймаут)")

    except Exception as e:
        print(f"Ошибка в фоновом ожидании платежа {payment_id}: {e}")


async def _poll_payment(payment_id: str, user_id: int, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler, data: dict, payment_type: str, interval: int):
    """
    Цикл опроса статуса платежа.
    Завершается, когда платёж оплачен.
    """
    while True:
        if payment_type == 'crypto':
            status = await check_oxa_payment(payment_id)
        else:
            status = False
        if status:
            await bot.send_message(
                chat_id=user_id,
                text='✅Оплата прошла успешно'
            )
            await execute_rate(user_id, bot, session, scheduler, data)
            await session.update_statistics('buys_sum', data.get('price'))
            await session.update_statistics('today_buys', data.get('price'))
            break
        await asyncio.sleep(interval)


async def execute_rate(user_id: int, bot: Bot, session: DataInteraction, scheduler: AsyncIOScheduler, data: dict):
    rate = data.get('rate')
    user = await session.get_user(user_id)
    if rate in ['vip', 'basic']:
        text = get_form_text(user.username, data)
        photo = data.get('photo_id')
        channel = data.get('channel')
        if channel == 'Mahram':
            if photo:
                await bot.send_photo(
                    chat_id=config.channels.makram,
                    photo=photo,
                    caption=text
                )
            else:
                await bot.send_message(
                    chat_id=config.channels.makram,
                    text=text
                )
        elif channel == 'NIKAH':
            if photo:
                await bot.send_photo(
                    chat_id=config.channels.nikah,
                    photo=photo,
                    caption=text
                )
            else:
                await bot.send_message(
                    chat_id=config.channels.nikah,
                    text=text
                )
        else:
            if photo:
                for channel in [config.channels.nikah, config.channels.makram]:
                    await bot.send_photo(
                        chat_id=channel,
                        photo=photo,
                        caption=text
                    )
            else:
                for channel in [config.channels.nikah, config.channels.makram]:
                    await bot.send_message(
                        chat_id=channel,
                        text=text
                    )
        await session.update_statistics('uploads_sum', 1)
        await session.update_statistics('today_uploads', 1)
        await bot.send_message(
            chat_id=user_id,
            text='🕙Ваша анкета будет выложена в порядке очереди'
        )
    else:
        channels = chats[rate]
        if isinstance(channels, list):
            text = ('Ваш доступ ко всем каналам👇\n\n<b>❗️Все ссылки на вступление одноразовые, '
                    'заявки в канал принимаются автоматически</b>')
            buttons = []
            counter = 1
            for channel in channels:
                url = await bot.create_chat_invite_link(
                    chat_id=channel,
                    expire_date=None,
                    member_limit=1
                )
                buttons.append(
                    [InlineKeyboardButton(text=f'Ссылка {counter}', url=url.invite_link)]
                )
            keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
            for channel in channels:
                if await session.get_user_channel(user_id, channel):
                    await session.update_channel_sub(user, channel)
                else:
                    await session.add_channel(user_id, channel, chats_title[channel])
        else:
            text = ('Ваш доступ в закрытый канал👇\n\n<b>❗️Ссылка на вступление в канал одноразовая, '
                    'заявки в канал принимаются автоматически</b>')
            url = await bot.create_chat_invite_link(
                chat_id=channels,
                expire_date=None,
                member_limit=1
            )
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='➡️ Вступить', url=url.invite_link)]]
            )
            if await session.get_user_channel(user_id, channels):
                await session.update_channel_sub(user_id, channels)
            else:
                await session.add_channel(user_id, channels, chats_title[channels])
        job_id = f'check_sub_{user_id}'
        job = scheduler.get_job(job_id=job_id)
        if job:
            job.remove()
        scheduler.add_job(
            check_sub,
            'interval',
            args=[user_id, bot, scheduler, session],
            id=job_id,
            days=1
        )
        await bot.send_message(
            chat_id=user_id,
            text=text,
            reply_markup=keyboard
        )

