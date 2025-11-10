from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.payment_dialog import getters

from states.state_groups import startSG, SurveySG, PaymentSG


payment_dialog = Dialog(
    Window(
        Const('🏦Выберите тип оплаты'),
        Column(
            Button(Const('💳Карта'), id='card_payment_choose', on_click=getters.payment_choose),
            #Button(Const('💲Крипта'), id='crypto_payment_choose', on_click=getters.payment_choose),
            #Button(Const('⭐️Звезды'), id='stars_payment_choose', on_click=getters.payment_choose),
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        state=PaymentSG.payment_type
    ),
    Window(
        Const('Для оплаты перейдите по ссылке ниже👇'
              '\n\t<em>После оплаты дождитесь подтверждения.</em>\n'
              '<b>❗️Счет будет действителен в течение 30 минут</b>'),
        Column(
            Url(Format('🔗Оплатить'), id='payment_link', url=Format('{url}')),
        ),
        Button(Format('⬅️Назад'), id='back_payment_type', on_click=getters.close_poll_payment),
        getter=getters.card_payment_getter,
        state=PaymentSG.card_payment
    ),
    Window(
        Const('Для оплаты перейдите по ссылке ниже👇'
              '\n\t<em>После оплаты дождитесь подтверждения.</em>\n'
              '<b>❗️Счет будет действителен в течение 30 минут</b>'),
        Column(
            Url(Format('🔗Оплатить'), id='payment_link', url=Format('{url}')),
        ),
        Button(Format('⬅️Назад'), id='back_payment_type', on_click=getters.close_poll_payment),
        getter=getters.crypto_payment_getter,
        state=PaymentSG.crypto_payment
    ),
)