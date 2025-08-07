from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.survey_dialogs.women_dialog import getters

from states.state_groups import SurveySG, WomenSurveySG


women_survey_dialog = Dialog(
    Window(
        Const('На каких языках вы говорите'),
        TextInput(
            id='get_languages',
            on_success=getters.get_languages
        ),
        Button(Const('⬅️Назад'), id='close_dialog', on_click=getters.close_dialog),
        state=WomenSurveySG.get_languages
    ),
    Window(
        Const('Были ли у вас какие либо отношения с мужчиной ?'),
        Row(
            Button(Const('Да'), id='yes_relation_choose', on_click=getters.relation_choose),
            Button(Const('Нет'), id='no_relation_choose', on_click=getters.relation_choose),
        ),
        Back(Const('⬅️Назад'), id='back_get_languages'),
        state=WomenSurveySG.is_relation
    ),
    Window(
        Const('Укажите свою религию'),
        TextInput(
            id='get_religion',
            on_success=getters.get_religion
        ),
        SwitchTo(Const('⬅️Назад'), id='back_is_relation', state=WomenSurveySG.is_relation),
        state=WomenSurveySG.get_religion
    ),
    Window(
        Const('Вы совершаете намаз? (текст в свободной форме)'),
        TextInput(
            id='get_prayer_text',
            on_success=getters.get_prayer_text
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_religion', state=WomenSurveySG.get_religion),
        state=WomenSurveySG.is_prayer
    ),
    Window(
        Const('Вы состояли в браке?'),
        Row(
            Button(Const('Да'), id='yes_married_choose', on_click=getters.choose_is_married),
            Button(Const('Нет'), id='no_married_choose', on_click=getters.choose_is_married),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_is_prayer', state=WomenSurveySG.is_prayer),
        state=WomenSurveySG.is_married
    ),
    Window(
        Const('Готовы ли вы пойти второй женой, если брат обеспеченный'),
        Row(
            Button(Const('Да'), id='yes_second_wife_choose', on_click=getters.second_wife_choose),
            Button(Const('Нет'), id='no_second_wife_choose', on_click=getters.second_wife_choose),
        ),
        Back(Const('⬅️Назад'), id='back_is_ralation'),
        state=WomenSurveySG.is_second_wife
    ),
    Window(
        Const('Готовы ли вы на переезд'),
        Row(
            Button(Const('Да'), id='yes_removal_choose', on_click=getters.removal_choose),
            Button(Const('Нет'), id='no_removal_choose', on_click=getters.removal_choose),
        ),
        Back(Const('⬅️Назад'), id='back_is_second_wife'),
        state=WomenSurveySG.get_removal
    ),
    Window(
        Const('Введите свой номер телефона или другие контактные данные для дальнейшей с вами связи'),
        TextInput(
            id='get_phone',
            on_success=getters.get_phone
        ),
        Back(Const('⬅️Назад'), id='back_get_removal'),
        state=WomenSurveySG.get_phone
    ),
    Window(
        Const('Отправьте одно свое фото'),
        MessageInput(
            func=getters.get_photo,
            content_types=ContentType.PHOTO
        ),
        SwitchTo(Const('Пропустить'), id='skip_get_photo', state=WomenSurveySG.choose_channel),
        Back(Const('⬅️Назад'), id='back_get_phone'),
        state=WomenSurveySG.get_photo
    ),
    Window(
        Format('{text}'),
        Column(
            Button(Const('Проект Mahram'), id='mahram_channel_choose', on_click=getters.channel_choose),
            Button(Const('Проект Nikah'), id='nikah_channel_choose', on_click=getters.channel_choose),
            Button(Const('Оба канала'), id='both_channel_choose', on_click=getters.channel_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_photo', state=WomenSurveySG.get_photo),
        getter=getters.choose_channel_getter,
        state=WomenSurveySG.choose_channel
    ),
)