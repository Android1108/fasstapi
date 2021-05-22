from aiogram import Bot
from telegram_bot.settings import settings

bot = Bot(
    token=settings.TELEGRAM_BOT_API_KEY,
    # proxy=settings.PROXY
)
