import hashlib
import hmac
import json
import time
import logging

from urllib.parse import parse_qs
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings

from .models import TelegramUser

logger = logging.getLogger(__name__)


class TelegramAuth(BaseAuthentication):
    """
    DRF Authentication class for Telegram Mini Apps.

    Reads the X-Telegram-Init-Data header, verifies the HMAC-SHA256
    signature using the bot token, then returns or creates the user.

    In DEBUG mode (or when no initData is present), falls back to a
    development test user so you can use DRF Browsable API / curl freely.
    """

    # How old an initData payload is allowed to be (seconds).
    # Telegram recommends rejecting anything older than 1 day.
    MAX_AUTH_DATE_AGE = 86400  # 24 hours

    def authenticate(self, request):
        init_data = request.headers.get("X-Telegram-Init-Data", "").strip()
        if not init_data:
            if getattr(settings, "DEBUG", False):
                logger.debug("No initData header — returning dev user (DEBUG=True)")
                dev_user, _ = TelegramUser.objects.get_or_create(
                    telegram_id=123456789,
                    defaults={
                        "first_name": "Dev",
                        "username": "dev_user",
                    },
                )
                return (dev_user, None)
            else:
                return None

        try:
            parsed = parse_qs(init_data, keep_blank_values=True, strict_parsing=False)
        except Exception as exc:
            logger.warning("Failed to parse initData: %s", exc)
            raise exceptions.AuthenticationFailed("Malformed initData")

        received_hash_list = parsed.pop("hash", None)
        if not received_hash_list or not received_hash_list[0]:
            raise exceptions.AuthenticationFailed("initData missing 'hash' field")

        received_hash = received_hash_list[0]

        data_check_string = "\n".join(
            f"{key}={values[0]}"
            for key, values in sorted(parsed.items())
        )

        bot_token = settings.TELEGRAM_BOT_TOKEN
        secret_key = hmac.new(
            b"WebAppData",
            bot_token.encode(),
            hashlib.sha256,
        ).digest()

        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(calculated_hash, received_hash):
            logger.warning(
                "Telegram hash mismatch. "
                "Expected=%s  Got=%s  data_check_string=%r",
                calculated_hash[:12] + "…",
                received_hash[:12] + "…",
                data_check_string[:80],
            )

            if getattr(settings, "DEBUG", False):
                logger.warning("⚠️  Hash invalid but DEBUG=True — returning dev user")
                dev_user, _ = TelegramUser.objects.get_or_create(
                    telegram_id=123456789,
                    defaults={"first_name": "Dev", "username": "dev_user"},
                )
                return (dev_user, None)
            else:
                raise exceptions.AuthenticationFailed("Invalid Telegram signature")

        auth_date_values = parsed.get("auth_date")
        if auth_date_values:
            try:
                auth_date = int(auth_date_values[0])
                age = int(time.time()) - auth_date
                if age > self.MAX_AUTH_DATE_AGE:
                    logger.warning("initData expired: auth_date is %d seconds old", age)
                    raise exceptions.AuthenticationFailed(
                        "initData has expired. Please reopen the Mini App."
                    )
            except ValueError:
                logger.warning("auth_date field is not an integer: %r", auth_date_values[0])

        user_json_list = parsed.get("user")
        if not user_json_list or not user_json_list[0]:
            raise exceptions.AuthenticationFailed("initData missing 'user' field")

        try:
            user_data = json.loads(user_json_list[0])
        except json.JSONDecodeError as exc:
            logger.warning("Failed to parse user JSON: %s", exc)
            raise exceptions.AuthenticationFailed("Invalid user JSON in initData")

        telegram_id = user_data.get("id")
        if not telegram_id:
            raise exceptions.AuthenticationFailed("user.id missing in initData")

        first_name  = user_data.get("first_name", "")
        last_name   = user_data.get("last_name", "")
        username    = user_data.get("username", "")
        language_code = user_data.get("language_code", "")

        user, created = TelegramUser.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "language_code": language_code,
            },
        )

        logger.info(
            "%s Telegram user: id=%s name=%s username=%s",
            "Created" if created else "Updated",
            telegram_id,
            first_name,
            username or "(none)",
        )

        return (user, None)