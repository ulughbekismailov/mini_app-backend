from django.db import models
from django.utils import timezone
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sold_count = models.PositiveIntegerField(default=0)

    discount_percent = models.PositiveIntegerField(null=True, blank=True)
    discount_start = models.DateTimeField(null=True, blank=True)
    discount_end = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def main_image(self):
        return self.images.filter(is_main=True).first()

    @property
    def all_images(self):
        return self.images.all().order_by('order', 'created_at')

    def increase_sold_count(self, quantity):
        self.sold_count += quantity
        self.save()

    def get_final_price(self):
        now = timezone.now()
        if self.discount_percent and self.discount_start and self.discount_end:
            if self.discount_start <= now <= self.discount_end:
                return self.price * (Decimal(1) - self.discount_percent / Decimal(100))
        return self.price

    def __str__(self):
        return self.name

    @property
    def is_discount_active(self):

        if not all([self.discount_percent, self.discount_start, self.discount_end]):
            return False

        now = timezone.now()

        return self.discount_start <= now <= self.discount_end
