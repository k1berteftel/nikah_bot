from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.survey_dialogs import getters

from states.state_groups import SurveySG


survey_dialog = Dialog(
    Window(
        Const('Введите свое Имя (Как к вам можно обращаться)'),
        TextInput(
            id='get_name',
            on_success=getters.get_name
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        state=SurveySG.get_name
    ),
    Window(
        Const('Введите свой возраст'),
        TextInput(
            id='get_age',
            on_success=getters.get_age
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_name', state=SurveySG.get_name),
        state=SurveySG.get_age
    ),
    Window(
        Const('Введите свой город'),
        TextInput(
            id='get_city',
            on_success=getters.get_city
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_age', state=SurveySG.get_age),
        state=SurveySG.get_city
    ),
    Window(
        Const('Введите свою национальность'),
        TextInput(
            id='get_origin',
            on_success=getters.get_origin
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_city', state=SurveySG.get_city),
        state=SurveySG.get_origin
    ),
    Window(
        Const('Укажите свой рост'),
        TextInput(
            id='get_height',
            on_success=getters.get_height
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_origin', state=SurveySG.get_origin),
        state=SurveySG.get_height
    ),
    Window(
        Const('Укажите свой вес'),
        TextInput(
            id='get_weight',
            on_success=getters.get_weight
        ),
        SwitchTo(Const('⬅️Назад'), id='back_get_height', state=SurveySG.get_height),
        state=SurveySG.get_weight
    ),
    Window(
        Const('У вас есть дети?\nЕсли есть введите их кол-во'),
        TextInput(
            id='get_children_count',
            on_success=getters.get_children_count
        ),
        SwitchTo(Const('Нет'), id='is_islam_switcher', state=SurveySG.get_about),
        SwitchTo(Const('⬅️Назад'), id='back_get_weight', state=SurveySG.get_weight),
        state=SurveySG.has_children
    ),
    Window(
        Const('Напишите немного о себе в свободной форме'),
        TextInput(
            id='get_about',
            on_success=getters.get_about
        ),
        SwitchTo(Const('⬅️Назад'), id='back_has_children', state=SurveySG.has_children),
        state=SurveySG.get_about
    ),
)