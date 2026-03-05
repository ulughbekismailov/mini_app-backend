from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Order
from telegram_bot.services.notifications import notify_user_delivered
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, created, **kwargs):

    if created:
        return

    try:
        order = Order.objects.get(pk=instance.pk)
        confirmed = order.confirmed_by_user
        new_status = order.status
    except Order.DoesNotExist:
        return

    if new_status == 'Delivered' and confirmed == False:
        logger.info(f"📦 Order #{instance.id} delivered bo'ldi - user ga xabar yuborilmoqda")
        notify_user_delivered(instance)
        print("Userga xabar yuborilmoqda")
    else:
        return


