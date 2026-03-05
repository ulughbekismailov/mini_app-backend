# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from products.models import Order, Product
#
#
# @receiver(post_save, sender=Order)
# def update_sold_count(sender, instance, created, **kwargs):
#
#     if created:
#         return
#
#     try:
#         order = Order.objects.get(pk=instance.pk)
#         new_status = order.status
#
#     except Order.DoesNotExist:
#         return
#
#     if new_status == 'Delivered':
#         for item in instance.items.all():
#             product = Product.objects.get(id=item.product_id)
#             product.sold_count += item.quantity
#             product.save()
#             print("Bizda hamma si ishladi count uchun>>>>>>>>>")