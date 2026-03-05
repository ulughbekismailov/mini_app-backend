from django.db import models
from .tg_user import TelegramUser
from .micro import Product


class ProductLike(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
