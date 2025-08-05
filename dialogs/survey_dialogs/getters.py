from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, SurveySG, MenSurveySG, WomenSurveySG

# поменять showmode


async def get_name(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.clear()
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    await msg.delete()
    dialog_manager.dialog_data['name'] = text
    await dialog_manager.switch_to(SurveySG.get_age, show_mode=ShowMode.DELETE_AND_SEND)


async def get_age(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    try:
        age = int(text)
    except Exception:
        await msg.answer('Возраст должен быть числом, пожалуйста попробуйте еще раз')
        return
    if age < 18:
        await msg.answer('Извините, но создавать анкету можно только с 18 лет')
        dialog_manager.dialog_data.clear()
        await dialog_manager.done()
        return
    dialog_manager.dialog_data['age'] = age
    await dialog_manager.switch_to(SurveySG.get_city, show_mode=ShowMode.DELETE_AND_SEND)


async def get_city(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['city'] = text
    await dialog_manager.switch_to(SurveySG.get_origin, show_mode=ShowMode.DELETE_AND_SEND)


async def get_origin(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['origin'] = text
    await dialog_manager.switch_to(SurveySG.get_height, show_mode=ShowMode.DELETE_AND_SEND)


async def get_height(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    try:
        height = int(text)
    except Exception:
        await msg.answer('Рост должен быть числом, пожалуйста попробуйте еще раз')
        return
    dialog_manager.dialog_data['height'] = height
    await dialog_manager.switch_to(SurveySG.get_weight, show_mode=ShowMode.DELETE_AND_SEND)


async def get_weight(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    try:
        weight = int(text)
    except Exception:
        await msg.answer('Вес должен быть числом, пожалуйста попробуйте еще раз')
        return
    dialog_manager.dialog_data['weight'] = weight
    await dialog_manager.switch_to(SurveySG.has_children, show_mode=ShowMode.DELETE_AND_SEND)


async def get_children_count(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    try:
        children = int(text)
    except Exception:
        await msg.answer('Кол-во детей должно быть числом, пожалуйста попробуйте еще раз')
        return
    dialog_manager.dialog_data['children'] = children
    await dialog_manager.switch_to(SurveySG.get_about, show_mode=ShowMode.DELETE_AND_SEND)


async def get_about(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['about'] = text
    male = dialog_manager.dialog_data.get('male')
    data = {}
    if dialog_manager.start_data:
        data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    data.update(dialog_manager.dialog_data)
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
        except Exception:
            ...
        counter = 1
        while dialog_manager.has_context():
            await dialog_manager.done()
            try:
                await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id + counter)
            except Exception:
                ...
            counter += 1
    if male:
        await dialog_manager.start(MenSurveySG.get_work, data=data, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(WomenSurveySG.get_languages, data=data, mode=StartMode.RESET_STACK)

