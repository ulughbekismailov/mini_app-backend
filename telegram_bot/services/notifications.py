import logging
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from asgiref.sync import async_to_sync, sync_to_async

logger = logging.getLogger(__name__)

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN

@sync_to_async
def get_user_telegram_id(order):
    try:
        if order.customer:
            return order.customer.telegram_id
        return None
    except AttributeError:
        return None
    except Exception as e:
        logger.error(f"Xatolik: {e}")
        return None



async def send_delivery_notification(order_id, order_total, user_telegram_id):

    bot = Bot(BOT_TOKEN)

    keyboard = [[
        InlineKeyboardButton(
            text="✅ Yetib keldi",
            callback_data=f"confirm_{order_id}"
        )
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await bot.send_message(
            chat_id=user_telegram_id,
            text=(
                f"📦 **Buyurtmangiz yetib keldi!**\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"🆔 Buyurtma #{order_id}\n"
                f"💰 Jami: ${order_total}\n"
                f"━━━━━━━━━━━━━━━━\n"
                f"Iltimos, tasdiqlash tugmasini bosing:"
            ),
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        logger.info(f"✅ User {user_telegram_id} ga xabar yuborildi (order #{order_id})")
        return True
    except Exception as e:
        logger.error(f"❌ Xatolik xabar yuborishda: {e}")
        return False


def notify_user_delivered(order):
    try:
        user_id = async_to_sync(get_user_telegram_id)(order)

        if not user_id:
            logger.warning(f"⚠️ Order #{order.id} userida telegram ID yo'q")
            return False

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(
            send_delivery_notification(order.id, order.total_price, user_id)
        )

        loop.close()
        logger.info(f"✅ Order #{order.id} uchun xabar yuborildi")
        return True
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}")
        return False
