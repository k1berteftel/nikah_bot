from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.admin_dialog import getters
from states.state_groups import adminSG


admin_dialog = Dialog(
    Window(
        Const('Админ панель'),
        Column(
            Button(Const('📊 Получить статистику'), id='get_static', on_click=getters.get_static),
            SwitchTo(Const('🛫Сделать рассылку'), id='mailing_menu_switcher', state=adminSG.get_mail),
            SwitchTo(Const('🔗 Управление диплинками'), id='deeplinks_menu_switcher', state=adminSG.deeplink_menu),
            SwitchTo(Const('👥 Управление админами'), id='admin_menu_switcher', state=adminSG.admin_menu),
            SwitchTo(Const('Управление ОП'), id='op_menu_switcher', state=adminSG.op_menu),
            SwitchTo(Const('Управление автоприемом'), id='accept_menu_switcher', state=adminSG.accept_menu),
            SwitchTo(Const('Добавить скидки'), id='discount_menu_switcher', state=adminSG.discount_menu),
            Button(Const('📋Выгрузка базы пользователей'), id='get_users_txt', on_click=getters.get_users_txt),
        ),
        Cancel(Const('Назад'), id='close_admin'),
        state=adminSG.start
    ),
    Window(
        Format('📋 *Меню управления Автоприемом*\n\n'
               '📋 *Действующие каналы*:\n\n {buttons}'),
        Column(
            SwitchTo(Const('➕ Добавить канал'), id='get_accept_channel_switcher', state=adminSG.get_accept_channel),
        ),
        Group(
            Select(
                Format('💼 {item[0]}'),
                id='accept_channel_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.accept_channel_selector
            ),
            width=1
        ),
        SwitchTo(Const('🔙 Назад'), id='back', state=adminSG.start),
        getter=getters.accept_menu_getter,
        state=adminSG.accept_menu
    ),
    Window(
        Const("Отправьте chat ID канала куда надо принимать заявки и отправлять текст\n\n"
              "<b>❗️Перед этим добавьте бота в канал и назначьте админом, со всеми правами</b>"),
        TextInput(
            id='get_accept_channel_id',
            on_success=getters.get_accept_channel_id
        ),
        SwitchTo(Const('Назад'), id='back_accept_menu', state=adminSG.accept_menu),
        state=adminSG.get_accept_channel
    ),
    Window(
        Const("Отправьте текст, который будет отправляться при приеме в канал"),
        TextInput(
            id='get_accept_text',
            on_success=getters.get_accept_text
        ),
        SwitchTo(Const('Назад'), id='back_get_accept_channel', state=adminSG.get_accept_channel),
        state=adminSG.get_accept_text
    ),
    Window(
        Format('Канал {channel_name}\nВсего принято в канал: {crossed}\n\n'
               'Текст при приеме в канал:\n{text}'),
        SwitchTo(Const('Изменить текст'), id='change_accept_text_switcher', state=adminSG.change_accept_text),
        Button(Const('Удалить канал для автоприема'), id='del_accept_channel', on_click=getters.del_accept_channel),
        SwitchTo(Const('Назад'), id='back_accept_menu', state=adminSG.accept_menu),
        getter=getters.accept_channel_menu_getter,
        state=adminSG.accept_channel_menu
    ),
    Window(
        Const("Отправьте новый текст, который будет отправляться при приеме в канал"),
        TextInput(
            id='change_accept_text',
            on_success=getters.change_accept_text
        ),
        SwitchTo(Const('Назад'), id='back_accept_channel_menu', state=adminSG.accept_channel_menu),
        state=adminSG.change_accept_text
    ),
    Window(
        Format('Меню активации скидок, действующая скидка: {discount}'),
        Column(
            Button(Format('{discount_action}'), id='toggle_discount', on_click=getters.toggle_discount),
        ),
        SwitchTo(Const('🔙Назад'), id='back', state=adminSG.start),
        getter=getters.discount_menu_getter,
        state=adminSG.discount_menu
    ),
    Window(
        Const('Введите процент скидки, который вы хотели бы добавить ко всем товарам бота'),
        TextInput(
            id='get_discount',
            on_success=getters.get_discount
        ),
        SwitchTo(Const('🔙 Назад'), id='back_discount_menu', state=adminSG.discount_menu),
        state=adminSG.get_discount
    ),
    Window(
        Format('🔗 *Меню управления диплинками*\n\n'
               '🎯 *Имеющиеся диплинки*:\n{links}'),
        Column(
            Button(Const('➕ Добавить диплинк'), id='add_deeplink', on_click=getters.add_deeplink),
            SwitchTo(Const('❌ Удалить диплинки'), id='del_deeplinks', state=adminSG.deeplink_del),
        ),
        SwitchTo(Const('🔙 Назад'), id='back', state=adminSG.start),
        getter=getters.deeplink_menu_getter,
        state=adminSG.deeplink_menu
    ),
    Window(
        Const('❌ Выберите диплинк для удаления'),
        Group(
            Select(
                Format('🔗 {item[0]}'),
                id='deeplink_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.del_deeplink
            ),
            width=1
        ),
        SwitchTo(Const('🔙 Назад'), id='deeplinks_back', state=adminSG.deeplink_menu),
        getter=getters.del_deeplink_getter,
        state=adminSG.deeplink_del
    ),
    Window(
        Format('👥 *Меню управления администраторами*\n\n {admins}'),
        Column(
            SwitchTo(Const('➕ Добавить админа'), id='add_admin_switcher', state=adminSG.admin_add),
            SwitchTo(Const('❌ Удалить админа'), id='del_admin_switcher', state=adminSG.admin_del)
        ),
        SwitchTo(Const('🔙 Назад'), id='back', state=adminSG.start),
        getter=getters.admin_menu_getter,
        state=adminSG.admin_menu
    ),
    Window(
        Const('👤 Выберите пользователя, которого хотите сделать админом\n'
              '⚠️ Ссылка одноразовая и предназначена для добавления только одного админа'),
        Column(
            Url(Const('🔗 Добавить админа (ссылка)'), id='add_admin',
                url=Format('http://t.me/share/url?url=https://t.me/bot?start={id}')),  # поменять ссылку
            Button(Const('🔄 Создать новую ссылку'), id='new_link_create', on_click=getters.refresh_url),
            SwitchTo(Const('🔙 Назад'), id='back_admin_menu', state=adminSG.admin_menu)
        ),
        getter=getters.admin_add_getter,
        state=adminSG.admin_add
    ),
    Window(
        Const('❌ Выберите админа для удаления'),
        Group(
            Select(
                Format('👤 {item[0]}'),
                id='admin_del_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.del_admin
            ),
            width=1
        ),
        SwitchTo(Const('🔙 Назад'), id='back_admin_menu', state=adminSG.admin_menu),
        getter=getters.admin_del_getter,
        state=adminSG.admin_del
    ),
    Window(
        Const('Введите сообщение которое вы хотели бы разослать\n\n<b>Предлагаемый макросы</b>:'
              '\n{name} - <em>полное имя пользователя</em>'),
        MessageInput(
            content_types=ContentType.ANY,
            func=getters.get_mail
        ),
        SwitchTo(Const('Назад'), id='back', state=adminSG.start),
        state=adminSG.get_mail
    ),
    Window(
        Const('Введите дату и время в которое сообщение должно отправиться всем юзерам в формате '
              'час:минута:день:месяц\n Например: 18:00 10.02 (18:00 10-ое февраля)'),
        TextInput(
            id='get_time',
            on_success=getters.get_time
        ),
        SwitchTo(Const('Продолжить без отложки'), id='get_keyboard_switcher', state=adminSG.get_keyboard),
        SwitchTo(Const('Назад'), id='back_get_mail', state=adminSG.get_mail),
        state=adminSG.get_time
    ),
    Window(
        Const('Введите кнопки которые будут крепиться к рассылаемому сообщению\n'
              'Введите кнопки в формате:\n кнопка1 - ссылка1\nкнопка2 - ссылка2'),
        TextInput(
            id='get_mail_keyboard',
            on_success=getters.get_mail_keyboard
        ),
        SwitchTo(Const('Продолжить без кнопок'), id='confirm_mail_switcher', state=adminSG.confirm_mail),
        SwitchTo(Const('Назад'), id='back_get_time', state=adminSG.get_time),
        state=adminSG.get_keyboard
    ),
    Window(
        Const('Вы подтверждаете рассылку сообщения'),
        Row(
            Button(Const('Да'), id='start_malling', on_click=getters.start_malling),
            Button(Const('Нет'), id='cancel_malling', on_click=getters.cancel_malling),
        ),
        SwitchTo(Const('Назад'), id='back_get_keyboard', state=adminSG.get_keyboard),
        state=adminSG.confirm_mail
    ),
    Window(
        Const('🔗 Введите свою ссылку на канал или пропустите этот шаг, '
              'чтобы бот сам подобрал ссылку для канала или чата'),
        TextInput(
            id='get_button_link',
            on_success=getters.get_button_link
        ),
        Button(Const('⏭ Пропустить'), id='continue_no_link', on_click=getters.save_without_link),
        state=adminSG.get_button_link
    ),
    Window(
        Format('📋 *Меню управления ОП*\n\n'
               '📋 *Действующие каналы*:\n\n {buttons}'),
        Column(
            SwitchTo(Const('➕ Добавить канал'), id='get_op_channel_switcher', state=adminSG.get_op_channel),
        ),
        Group(
            Select(
                Format('💼 {item[0]}'),
                id='buttons_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.op_buttons_switcher
            ),
            width=1
        ),
        SwitchTo(Const('🔙 Назад'), id='back', state=adminSG.start),
        getter=getters.op_menu_getter,
        state=adminSG.op_menu
    ),
    Window(
        Const("Отправьте ссылку канал (если он открытый) или его chat ID если канал закрытый\n\n"
              "<b>❗️Перед этим добавьте бота в канал и назначьте админом, со всеми правами</b>"),
        TextInput(
            id='get_op_chat_id',
            on_success=getters.get_op_channel
        ),
        SwitchTo(Const('Назад'), id='back_op_menu', state=adminSG.op_menu),
        state=adminSG.get_op_channel
    ),
    Window(
        Format('Канал|Чат {channel_name}\nУказанная ссылка на канал|чат: {channel_link}'),
        SwitchTo(Const('Изменить ссылку на канал'), id='change_button_link_switcher', state=adminSG.change_button_link),
        Button(Const('➖Удалить канал с ОП'), id='del_op_channel', on_click=getters.del_op_channel),
        SwitchTo(Const('Назад'), id='back_op_menu', state=adminSG.op_menu),
        getter=getters.button_menu_getter,
        state=adminSG.button_menu
    ),
    Window(
        Const('🔗 Введите новую ссылку для кнопки\n\n'
              '⚠️ <em>Важно: ссылка должна вести на тот же канал, иначе могут возникнуть проблемы с проверкой ОП</em>'),
        TextInput(
            id='change_button_link',
            on_success=getters.change_button_link
        ),
        state=adminSG.change_button_link
    ),
)