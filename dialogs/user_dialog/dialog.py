from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog import getters

from states.state_groups import startSG, SurveySG, adminSG

user_dialog = Dialog(
    Window(
        Format('{text}'),
        Column(
            SwitchTo(Const('📋Разместить анкету'), id='choose_male_switcher', state=startSG.choose_male),
            SwitchTo(Const('🔒 Купить доступ в приватные каналы'), id='private_menu_switcher', state=startSG.private_menu),
            #Url(Const('✍️Связаться с поддержкой'), id='support_url', url=Const('')),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        disable_web_page_preview=True,
        getter=getters.start_getter,
        state=startSG.start
    ),
    Window(
        Const('Какую анкету вы заполняете? <em>(Какого вы пола?)</em>'),
        Column(
            SwitchTo(Const('Мужская анкета'), id='choose_form_rate_switcher', state=startSG.choose_form_rate),
            Start(Const('Женская анкета'), id='women_form_start', state=SurveySG.get_name)
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.choose_male
    ),
    Window(
        Format('{text}'),
        Column(
            Button(Const('Обычная анкета'), id='basic_form_choose', on_click=getters.rate_choose),
            Button(Const('👑VIP-анкета'), id='vip_form_choose', on_click=getters.rate_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_male', state=startSG.choose_male),
        getter=getters.choose_form_rate_getter,
        state=startSG.choose_form_rate
    ),
    Window(
        Format('{text}'),
        Column(
            Button(Format('Девушки 23+ {price}₽)'), id='23plus_private_choose', on_click=getters.private_choose),
            Button(Format('Девушки до 23 {price}₽'), id='23minus_private_choose', on_click=getters.private_choose),
            Button(Format('Готовы стать второй женой {price}₽'), id='second_private_choose', on_click=getters.private_choose),
            Button(Format('Девушки из Дагестана {price}₽'), id='dagestan_private_choose', on_click=getters.private_choose),
            Button(Format('Девушки из Казахстана и Кыргызстана {price}₽'), id='kazakh_private_choose', on_click=getters.private_choose),
            Button(Format('🔥Спецпредложение! {special_price}₽'), id='special_private_choose', on_click=getters.private_choose),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.private_menu_getter,
        state=startSG.private_menu
    ),
)