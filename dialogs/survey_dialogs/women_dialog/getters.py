from aiogram import Bot
from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from utils.text_utils import get_form_text
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, SurveySG, WomenSurveySG


config: Config = load_config()


async def forward_form(bot: Bot, text: str, channel: str, photo: str | None):
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


async def close_dialog(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    if dialog_manager.start_data:
        data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    await dialog_manager.done()
    await dialog_manager.start(SurveySG.get_about, data=data, mode=StartMode.RESET_STACK)


async def get_languages(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    await msg.delete()
    dialog_manager.dialog_data['languages'] = text
    await dialog_manager.switch_to(WomenSurveySG.is_relation, show_mode=ShowMode.DELETE_AND_SEND)


async def relation_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    answer = clb.data.split('_')[0]
    if answer == 'yes':
        answer = 'Да'
    else:
        answer = 'Нет'
    dialog_manager.dialog_data['relation'] = answer
    await dialog_manager.switch_to(WomenSurveySG.get_religion, show_mode=ShowMode.DELETE_AND_SEND)


async def get_religion(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['religion'] = text
    await dialog_manager.switch_to(WomenSurveySG.is_prayer, show_mode=ShowMode.DELETE_AND_SEND)


async def get_prayer_text(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    await msg.delete()
    dialog_manager.dialog_data['prayer'] = text
    await dialog_manager.switch_to(WomenSurveySG.is_married, show_mode=ShowMode.DELETE_AND_SEND)


async def choose_is_married(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    answer = clb.data.split('_')[0]
    if answer == 'yes':
        answer = 'Да'
    else:
        answer = 'Нет'
    dialog_manager.dialog_data['married'] = answer
    await dialog_manager.switch_to(WomenSurveySG.is_second_wife, show_mode=ShowMode.DELETE_AND_SEND)


async def second_wife_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    answer = clb.data.split('_')[0]
    if answer == 'yes':
        dialog_manager.dialog_data['second_wife'] = 'Да'
    else:
        dialog_manager.dialog_data['second_wife'] = 'Нет'
    await dialog_manager.switch_to(WomenSurveySG.get_removal, show_mode=ShowMode.DELETE_AND_SEND)


async def removal_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    answer = clb.data.split('_')[0]
    if answer == 'yes':
        dialog_manager.dialog_data['removal'] = 'Да'
    else:
        dialog_manager.dialog_data['removal'] = 'Нет'
    await dialog_manager.switch_to(WomenSurveySG.get_photo, show_mode=ShowMode.DELETE_AND_SEND)


async def get_photo(msg: Message, widget: MessageInput, dialog_manager: DialogManager):
    await msg.delete()
    dialog_manager.dialog_data['photo_id'] = msg.photo[0].file_id
    await dialog_manager.switch_to(WomenSurveySG.choose_channel)


async def choose_channel_getter(dialog_manager: DialogManager, **kwargs):
    text = ('У нас два канала\n\n1) <a href="https://t.me/+dL5TzpGEcqllMTIy">Проект Mahram</a>\n'
            '2) <a href="https://t.me/+C7cuXHRxZgY0ZmE6">Проект NIKAH</a>\n\n'
            'Выберите в какой канал вы хотите выложить анкету')
    return {
        'text': text
    }


async def channel_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    channel = clb.data.split('_')[0]
    if channel == 'mahram':
        channel = 'Mahram'
    elif channel == 'nikah':
        channel = 'NIKAH'
    else:
        channel = 'Mahram и NIKAH'
    dialog_manager.dialog_data['channel'] = channel
    text = get_form_text(clb.from_user.username, dialog_manager.dialog_data)
    await forward_form(clb.bot, text, channel, dialog_manager.dialog_data.get('photo_id'))
    await clb.message.answer('🕙Ваша анкета будет выложена в порядке очереди')
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await clb.bot.delete_message(chat_id=clb.from_user.id, message_id=clb.message.message_id - 1)
        except Exception:
            ...
        counter = 1
        while dialog_manager.has_context():
            await dialog_manager.done()
            try:
                await clb.bot.delete_message(chat_id=clb.from_user.id, message_id=clb.message.message_id + counter)
            except Exception:
                ...
            counter += 1
    dialog_manager.dialog_data.clear()
    await dialog_manager.start(startSG.start, mode=StartMode.RESET_STACK)


