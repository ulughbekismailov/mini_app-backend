from telegram import Update
from telegram.ext import ContextTypes


async def my_orders_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Buyurtmalaringiz tez orada...")