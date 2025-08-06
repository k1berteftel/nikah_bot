from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, MenSurveySG, PaymentSG, SurveySG


rate_prices = {
    'basic': 1000,
    'vip': 3000
}


async def close_dialog(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    if dialog_manager.start_data:
        data.update(dialog_manager.start_data)
    await dialog_manager.done()
    await dialog_manager.start(SurveySG.get_about, data=data, mode=StartMode.RESET_STACK)


async def get_work(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    await msg.delete()
    dialog_manager.dialog_data['work'] = text
    await dialog_manager.switch_to(MenSurveySG.is_islam, show_mode=ShowMode.DELETE_AND_SEND)


async def cancel_survey(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    await clb.message.answer('<b>❗️Извините, в наших каналах выкладываются только Мусульманские анкеты</b>')
    dialog_manager.dialog_data.clear()
    await dialog_manager.done()
    await dialog_manager.start(startSG.start, mode=StartMode.RESET_STACK)


async def get_prayer_text(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['prayer'] = text
    await dialog_manager.switch_to(MenSurveySG.is_married, show_mode=ShowMode.DELETE_AND_SEND)


async def get_is_married(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['married'] = text
    await dialog_manager.switch_to(MenSurveySG.get_women_wishes, show_mode=ShowMode.DELETE_AND_SEND)


async def get_women_wishes(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['women_wishes'] = text
    await dialog_manager.switch_to(MenSurveySG.get_phone, show_mode=ShowMode.DELETE_AND_SEND)


async def get_phone(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['phone'] = text
    await dialog_manager.switch_to(MenSurveySG.get_photo, show_mode=ShowMode.DELETE_AND_SEND)


async def get_photo(msg: Message, widget: MessageInput, dialog_manager: DialogManager):
    await msg.delete()
    dialog_manager.dialog_data['photo_id'] = msg.photo[0].file_id
    await dialog_manager.switch_to(MenSurveySG.choose_channel, show_mode=ShowMode.DELETE_AND_SEND)


async def choose_channel_getter(dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    if dialog_manager.dialog_data.get('rate') == 'basic':
        price = 1000
        both_price = 1800
    else:
        price = 3000
        both_price = 5000
    discount = await session.get_discount()
    if discount:
        price = round(price - price * discount.percent / 100)
        both_price = round(both_price - both_price * discount.percent / 100)
    text = ('У нас два канала\n\n1) <a href="https://t.me/+dL5TzpGEcqllMTIy">Проект Mahram</a>\n'
            '2) <a href="https://t.me/+C7cuXHRxZgY0ZmE6">Проект NIKAH</a>\n\n'
            'Выберите в какой канал вы хотите выложить анкету')
    return {
        'text': text,
        'price': price,
        'both_price': both_price
    }


async def channel_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    channel = clb.data.split('_')[0]
    rate = dialog_manager.dialog_data.get('rate')
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    discount = await session.get_discount()
    price = 1000
    if channel == 'mahram':
        channel = 'Mahram'
    elif channel == 'nikah':
        channel = 'NIKAH'
    else:
        channel = 'Mahram и NIKAH'
        price = 1800
    if discount:
        price = round(price - price * discount.percent / 100)
    price = rate_prices[rate] + price
    data = {'channel': channel, 'price': price}
    data.update(dialog_manager.dialog_data)
    await dialog_manager.start(PaymentSG.payment_type, data=data)

