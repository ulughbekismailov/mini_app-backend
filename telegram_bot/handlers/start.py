import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from django.conf import settings
from asgiref.sync import sync_to_async

from products.models import TelegramUser

logger = logging.getLogger(__name__)


@sync_to_async
def get_user(telegram_id):
    try:
        return TelegramUser.objects.get(telegram_id=telegram_id)
    except TelegramUser.DoesNotExist:
        return None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    db_user = await get_user(user.id)

    if db_user:
        welcome_text = f"👋 Yana xush kelibsiz, {user.first_name}!"
    else:
        welcome_text = f"👋 Salom, {user.first_name}! Do'konimizga xush kelibsiz."

    keyboard = [[
        InlineKeyboardButton(
            text="🛍 Do'konni ochish",
            web_app={"url": settings.MINI_APP_URL}
        )
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        text=f"{welcome_text}\n\nDo'konni ochish uchun pastdagi tugmani bosing:👇",
        reply_markup=reply_markup
    )

    logger.info(f"👤 Foydalanuvchi @{user.username or user.id} start ishlatdi")