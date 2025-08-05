from dialogs.user_dialog.dialog import user_dialog
from dialogs.admin_dialog.dialog import admin_dialog
from dialogs.payment_dialog.dialog import payment_dialog
from dialogs.survey_dialogs import women_survey_dialog, men_survey_dialog, survey_dialog
from dialogs.sub_dialog.dialog import sub_dialog


def get_dialogs():
    return [user_dialog, sub_dialog, survey_dialog, men_survey_dialog, women_survey_dialog, payment_dialog, admin_dialog]