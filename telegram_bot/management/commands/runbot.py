# telegram_bot/management/commands/runbot.py
import logging
import sys
import traceback
import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.error import InvalidToken, Conflict, NetworkError

from telegram_bot.handlers import start, orders, callbacks

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Telegram botni ishga tushirish (polling mode)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Debug mode',
        )

    def handle(self, *args, **options):
        debug = options.get('debug', False)

        # Token tekshirish
        token = settings.TELEGRAM_BOT_TOKEN
        if not token:
            logger.critical("❌ TELEGRAM_BOT_TOKEN topilmadi! .env faylini tekshiring.")
            sys.exit(1)

        self.stdout.write(self.style.SUCCESS(f"🤖 Bot ishga tushmoqda... Token: {token[:8]}..."))

        try:
            # Botni yaratish
            app = Application.builder().token(token).build()

            # Handlerlarni qo'shish
            app.add_handler(CommandHandler("start", start.start_command))
            app.add_handler(CommandHandler("myorders", orders.my_orders_command))

            # Callback handlerlar
            app.add_handler(CallbackQueryHandler(
                callbacks.delivery_confirmation,
                pattern="^confirm_"
            ))
            app.add_handler(CallbackQueryHandler(
                callbacks.support_callback,
                pattern="^support_"
            ))

            # Bot ma'lumotlarini olish (sync usulda)
            import asyncio

            # Yangi event loop yaratish
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Bot ma'lumotlarini olish
            bot_info = loop.run_until_complete(app.bot.get_me())
            self.stdout.write(self.style.SUCCESS(
                f"✅ Bot @{bot_info.username} ishga tushdi!"
            ))

            # Polling mode
            self.stdout.write(self.style.WARNING("🔄 Polling mode da ishlayapti..."))

            # run_polling sync usulda - bu o'zi event loop yaratadi
            app.run_polling(
                drop_pending_updates=True,
                allowed_updates=['message', 'callback_query']
            )

        except InvalidToken:
            logger.critical("❌ Bot token yaroqsiz! TELEGRAM_BOT_TOKEN ni tekshiring.")
            sys.exit(1)
        except Conflict as e:
            logger.critical(f"❌ Bot conflict: {e}. Boshqa instance ishlayotgan bo'lishi mumkin.")
            sys.exit(1)
        except NetworkError as e:
            logger.critical(f"❌ Network error: {e}")
            sys.exit(1)
        except Exception as e:
            logger.critical(f"❌ Kutilmagan xatolik: {e}")
            traceback.print_exc()
            sys.exit(1)