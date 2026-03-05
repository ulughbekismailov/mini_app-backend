import logging
from telegram import Update
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async
from products.models import Product
from products.models import Order

logger = logging.getLogger(__name__)


@sync_to_async
def confirm_order_delivery(order_id):
    try:
        order = Order.objects.get(id=order_id)

        if order.status == 'Delivered':
            order.confirmed_by_user = True
            order.save()

            for item in order.items.all():
                product = Product.objects.get(id=item.product_id)
                product.sold_count += item.quantity
                product.save()

            return True, order

        return False, order

    except Order.DoesNotExist:
        return False, None


async def delivery_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    order_id = int(query.data.split('_')[1])

    success, order = await confirm_order_delivery(order_id)

    if success:
        await query.edit_message_text(
            text=f"✅ Buyurtma #{order_id} yetib kelgani tasdiqlandi!\n\nRahmat! Do'konimizdan sizni yana kutib qolamiz."
        )
        logger.info(f"✅ User @{update.effective_user.username} order #{order_id} ni tasdiqladi")
    else:
        await query.edit_message_text(
            text="❌ Xatolik yuz berdi yoki buyurtma allaqachon tasdiqlangan."
        )



async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Yordam so'rovingiz qabul qilindi")