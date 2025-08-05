from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.survey_dialogs.men_dialog import getters

from states.state_groups import MenSurveySG


men_survey_dialog = Dialog(
    Window(
        Const('Напишите немного о своей работе (кем, где работаете)'),
        TextInput(
            id='get_work',
            on_success=getters.get_work
        ),
        Button(Const('⬅️Назад'), id='close_dialog', on_click=getters.close_dialog),
        state=MenSurveySG.get_work
    ),
    Window(
        Const('Вы в Исламе?'),
        Row(
            SwitchTo(Const('Да'), id='is_prayer_switcher', state=MenSurveySG.is_prayer),
            Button(Const('Нет'), id='cancel_survey', on_click=getters.cancel_survey),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_children', state=MenSurveySG.get_work),
        state=MenSurveySG.is_islam
    ),
    Window(
        Const('Вы совершаете намаз? (текст в свободной форме)'),
        TextInput(
            id='get_prayer_text',
            on_success=getters.get_prayer_text
        ),
        SwitchTo(Const('⬅️Назад'), id='back_is_islam', state=MenSurveySG.is_islam),
        state=MenSurveySG.is_prayer
    ),
    Window(
        Const('Укажите ваше семейное положение'),
        TextInput(
            id='get_is_married',
            on_success=getters.get_is_married
        ),
        SwitchTo(Const('⬅️Назад'), id='back_is_islam', state=MenSurveySG.is_islam),
        state=MenSurveySG.is_married
    ),
    Window(
        Const('Введите свои пожелания по сестре (в свободной форме)'),
        TextInput(
            id='get_women_wishes',
            on_success=getters.get_women_wishes
        ),
        SwitchTo(Const('⬅️Назад'), id='back_is_married', state=MenSurveySG.is_married),
        state=MenSurveySG.get_women_wishes
    ),
    Window(
        Const('Введите свой номер телефона или другие контактные данные для дальнейшей с вами связи'),
        TextInput(
            id='get_phone',
            on_success=getters.get_phone
        ),
        SwitchTo(Const('⬅️Назад'), id='back_women_wishes', state=MenSurveySG.get_women_wishes),
        state=MenSurveySG.get_phone
    ),
    Window(
        Const('Отправьте одно свое фото'),
        MessageInput(
            func=getters.get_photo,
            content_types=ContentType.PHOTO
        ),
        SwitchTo(Const('Пропустить'), id='skip_photo', state=MenSurveySG.choose_channel),
        SwitchTo(Const('⬅️Назад'), id='back_get_phone', state=MenSurveySG.get_phone),
        state=MenSurveySG.get_photo
    ),
    Window(
        Format('{text}'),
        Column(
            Button(Format('Проект Mahram ({price}₽)'), id='mahram_channel_choose', on_click=getters.channel_choose),
            Button(Format('Проект Nikah ({price}₽)'), id='nikah_channel_choose', on_click=getters.channel_choose),
            Button(Format('Оба канала ({both_price}₽)'), id='both_channel_choose', on_click=getters.channel_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_photo', state=MenSurveySG.get_photo),
        getter=getters.choose_channel_getter,
        state=MenSurveySG.choose_channel
    ),
)