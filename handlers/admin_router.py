from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated
from aiogram_dialog import DialogManager, StartMode

from database.action_data_class import DataInteraction
from config_data.config import Config, load_config
from states.state_groups import adminSG


config: Config = load_config()
admin_router = Router()

pass