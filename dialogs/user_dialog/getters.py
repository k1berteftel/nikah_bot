from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, SurveySG, PaymentSG


config: Config = load_config()


async def start_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    admin = False
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if event_from_user.id in admins:
        admin = True
    text = ('<b>Ассаляму алейкум! 👋</b>\n\nДобро пожаловать в бот знакомств мусульман для создания семьи ! 🌙'
            '\n\nТак как у нас очень много желающих создать семью мы сделали два канала\n\n1 канал '
            '<a href="https://t.me/+dL5TzpGEcqllMTIy">Проект Махрам</a>.\n2 канал '
            '<a href="https://t.me/+C7cuXHRxZgY0ZmE6">Проект Никях</a>.\n\nЗдесь ты можешь:  '
            '\n\n<b>✅ Разместить анкету</b> — расскажи о себе и найди свою вторую половинку.\n\n\n'
            '🔒 Получить доступ к закрытому каналу где анкеты невест с их  контактами данными. '
            '( Все анкеты размещены с одобрения невест которые ищут мужа. ) \n\n📌 Выбирай действие ниже и начни '
            'свой путь к счастливым отношениям уже сегодня!\n\nВаш аккаунт и платежи полностью защищены.\n\n'
            ' Что ты хочешь сделать?')
    return {
        'text': text,
        'admin': admin
    }


async def choose_form_rate_getter(dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    basic = 1000
    vip = 3000
    discount = await session.get_discount()
    if discount:
        basic = round(basic - basic * discount.percent / 100)
        vip = round(vip - vip * discount.percent / 100)
    text = (f'У нас 2 варианта оформления анкеты:\n\n1) 📌 Обычная анкета ({basic} руб):\n'
            f'✔️ Публикуется 1 раз в ленте канала.\n✔️ Без специального оформления.\n'
            f'✔️ Подходит для тех, кто хочет просто попробовать.\n\n2) ✅ VIP-анкета ({vip} руб):\n✔️ Красивое'
            f' оформление с пометкой "VIP" (привлекает больше внимания).\n✔️ Публикуется 5 дней подряд в основном '
            f'канале (вас увидят все новые подписчики).\n✔️ Выделяется среди обычных анкет — больше  откликов.\n'
            f'\nВыберите тип анкеты:')
    return {'text': text}


async def rate_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    rate = clb.data.split('_')[0]
    start_data = {'rate': rate, 'male': 'men'}
    await dialog_manager.start(SurveySG.get_name, data=start_data)


async def private_menu_getter(dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    price = '10 000'
    special_price = '30 000'
    discount = await session.get_discount()
    if discount:
        price = round(int(price) - int(price) * discount.percent / 100)
        special_price = round(int(special_price) - int(special_price) * discount.percent / 100)
    text = (f'<b>🔥 Эксклюзивный доступ к приватным каналам с анкетами невест 🔥</b>\n\nХотите найти свою вторую '
            f'половинку без лишних хлопот? Мы предлагаем уникальную базу анкет девушек, которые готовы выйти замуж !'
            f'\n\n<b>Что входит в подписку?</b>\n\n✅ 5 закрытых каналов с проверенными анкетами\n✅ Фото и контакты '
            f'девушек (размещены с их согласия)\n✅  Ежедневное пополнение – минимум 3 новые анкеты в день\n'
            f'✅  Экономия до 90%** – вместо 90 000 руб. вы платите всего {price} руб. за канал !\n\n'
            f'    Выберите подходящий вариант:\n🔹 Девушки 23 +  – {price} руб.\n🔹 Девушки до 23 – {price} руб.\n'
            f'🔹 Готовы стать второй женой – {price} руб.\n🔹 Девушки из Дагестана – {price} руб.\n🔹 Девушки из '
            f'Казахстана – {price} руб.\n\n   <b> 💎 Спецпредложение! 🔥 ВСЕ 5 КАНАЛОВ (скидка 50%) – {special_price} руб.  '
            f'вместо 50 000 руб.</b>\n\n    Почему это выгодно?\n✔️ Быстрый доступ к проверенным девушкам\n'
            f'✔️ Экономия времени и денег – не нужно искать вручную\n✔️ Конфиденциально и безопасно\n\n'
            f'<b>💬 Оформляйте подписку сейчас и начните знакомство уже сегодня!</b>\n\n'
            f' Выберите канал, чтобы получить доступ! 👇')
    return {
        'text': text,
        'price': price,
        'special_price': special_price
    }


async def private_choose(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    discount = await session.get_discount()
    rate = clb.data.split('_')[0]
    price = 10000
    if rate == 'special':
        price = 30000
    if discount:
        price = round(price - price * discount.percent / 100)
    data = {
        'rate': rate,
        'price': price
    }
    await dialog_manager.start(PaymentSG.payment_type, data=data)