import asyncio

from aiogram.types import CallbackQuery, User, Message, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from utils.payments import get_yookassa_url, get_oxa_payment_data
from utils.process_payment import wait_for_payment
from utils.text_utils import get_form_text
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, SurveySG, PaymentSG

rates = {
    'vip': {
        'title': 'Публикация VIP анкеты',
        'description': 'Оплата публикации VIP анкеты',
        'payload': 'vip'
    },
    'basic': {
        'title': 'Публикация обычной анкеты',
        'description': 'Оплата публикации обычной анкеты',
        'payload': 'basic'
    },
    '23plus': {
        'title': 'Подписка на приватный канал',
        'description': 'Покупка входа в закрытый канал',
        'payload': '23plus'
    },
    '23minus': {
        'title': 'Подписка на приватный канал',
        'description': 'Покупка входа в закрытый канал',
        'payload': '23minus'
    },
    'second': {
        'title': 'Подписка на приватный канал',
        'description': 'Покупка входа в закрытый канал',
        'payload': 'second'
    },
    'dagestan': {
        'title': 'Подписка на приватный канал',
        'description': 'Покупка входа в закрытый канал',
        'payload': 'dagestan'
    },
    'kazakh': {
        'title': 'Подписка на приватный канал',
        'description': 'Покупка входа в закрытый канал',
        'payload': 'kazakh'
    },
    'special': {
        'title': 'Подписка пак приватных каналов',
        'description': 'Покупка входа во все закрытые каналы',
        'payload': 'special'
    }
}


async def process_payment():
    pass


async def payment_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    scheduler: AsyncIOScheduler = dialog_manager.middleware_data.get('scheduler')
    price = dialog_manager.dialog_data.get('price')
    rate = dialog_manager.dialog_data.get('rate')
    payment = clb.data.split('_')[0]
    if payment == 'card':
        payment = await get_yookassa_url(price, rates[rate].get("description"))
        task = asyncio.create_task(
            wait_for_payment(
                payment_id=payment.get('id'),
                user_id=clb.from_user.id,
                bot=clb.bot,
                session=session,
                scheduler=scheduler,
                payment_type='card',
                data=dialog_manager.dialog_data
            )
        )
        for active_task in asyncio.all_tasks():
            if active_task.get_name() == f'process_payment_{clb.from_user.id}':
                active_task.cancel()
        task.set_name(f'process_payment_{clb.from_user.id}')
        dialog_manager.dialog_data['card_url'] = payment.get('url')
        await dialog_manager.switch_to(PaymentSG.card_payment)
        return
    elif payment == 'crypto':
        payment = await get_oxa_payment_data(price)
        task = asyncio.create_task(
            wait_for_payment(
                payment_id=payment.get('id'),
                user_id=clb.from_user.id,
                bot=clb.bot,
                session=session,
                scheduler=scheduler,
                payment_type='crypto',
                data=dialog_manager.dialog_data
            )
        )
        for active_task in asyncio.all_tasks():
            if active_task.get_name() == f'process_payment_{clb.from_user.id}':
                active_task.cancel()
        task.set_name(f'process_payment_{clb.from_user.id}')
        dialog_manager.dialog_data['crypto_url'] = payment.get('url')
        await dialog_manager.switch_to(PaymentSG.crypto_payment)
        return
    else:
        state: FSMContext = dialog_manager.middleware_data.get('state')
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='Оплатить', pay=True)],
                [InlineKeyboardButton(text='Закрыть', callback_data='close_payment')]
            ]
        )
        await state.update_data(dialog_manager.dialog_data)
        price = int(round(price / 1.6, 0))
        prices = [LabeledPrice(label="XTR", amount=price)]
        rate_data = rates[rate]
        await clb.message.answer_invoice(
            title=rate_data['title'],
            description=rate_data['description'],
            payload=rate_data['payload'],
            currency="XTR",
            prices=prices,
            provider_token="",
            reply_markup=keyboard
        )


async def card_payment_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'url': dialog_manager.dialog_data.get("card_url")
    }


async def crypto_payment_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'url': dialog_manager.dialog_data.get("crypto_url")
    }


async def close_poll_payment(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    name = f'process_payment_{clb.from_user.id}'
    for task in asyncio.all_tasks():
        if task.get_name() == name:
            task.cancel()
    await dialog_manager.switch_to(PaymentSG.payment_type)
