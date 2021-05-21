
from aiogram import types

from telegram_bot.database import crud
from telegram_bot.database.database import get_db_session
from telegram_bot.intergration import he_weather
from telegram_bot.telegram.components.keyboard_markup_factory import KeyboardMarkUpFactory, WELCOME_TEXT
from telegram_bot.telegram.dispatcher import dp
from telegram_bot.telegram.finite_state_machine import update_location
from telegram_bot.telegram.service.message import TelegramMessageService

def registered(func):
    async def wrapper(message: types.Message):
        chat_id = message.chat.id
        with get_db_session() as db:
            user = crud.get_user(db, chat_id)

        if not user:
            return await update_location(message)

        await func(message)

    return wrapper

@dp.message_handler(commands=['weather'])
@registered
async def handle_weather(message: types.Message) -> None:
    chat_id = message.chat.id
    with get_db_session() as db:
        user = crud.get_user(db, chat_id)

    text = await he_weather.get_weather_forecast(user.location)
    await TelegramMessageService.send_text(dp.bot, chat_id, text)

@dp.message_handler(commands=['help', 'start'])
async def handle_help(message: types.Message) -> None:
    with get_db_session() as db:
        user = crud.get_user(db, message.chat.id)
    print("tset")
    reply_markup = KeyboardMarkUpFactory.build_main_menu(user)
    await TelegramMessageService.send_keyboard_markup(dp.bot, message.chat.id, WELCOME_TEXT, reply_markup)