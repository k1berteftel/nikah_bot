from aiogram.fsm.state import State, StatesGroup

# Обычная группа состояний


class startSG(StatesGroup):
    start = State()
    choose_male = State()
    choose_form_rate = State()
    private_menu = State()


class SurveySG(StatesGroup):
    get_name = State()
    get_age = State()
    get_city = State()
    get_origin = State()
    get_height = State()
    get_weight = State()
    has_children = State()
    get_about = State()


class MenSurveySG(StatesGroup):
    get_work = State()
    get_women_wishes = State()
    is_married = State()
    is_islam = State()
    is_prayer = State()
    get_phone = State()
    get_photo = State()
    choose_channel = State()


class WomenSurveySG(StatesGroup):
    is_relation = State()
    get_languages = State()
    get_religion = State()
    is_prayer = State()
    is_married = State()
    is_second_wife = State()
    get_removal = State()
    get_photo = State()
    choose_channel = State()


class PaymentSG(StatesGroup):
    payment_type = State()
    card_payment = State()
    crypto_payment = State()


class SubSG(StatesGroup):
    start = State()


class adminSG(StatesGroup):
    start = State()

    get_mail = State()
    get_time = State()
    get_keyboard = State()
    confirm_mail = State()

    deeplink_menu = State()
    deeplink_del = State()

    admin_menu = State()
    admin_del = State()
    admin_add = State()

    op_menu = State()
    get_op_channel = State()
    get_button_link = State()
    button_menu = State()
    change_button_text = State()
    change_button_link = State()

    discount_menu = State()
    get_discount = State()

    accept_menu = State()
    get_accept_channel = State()
    get_accept_text = State()
    accept_channel_menu = State()
    change_accept_text = State()

