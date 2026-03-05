from django.db import models
from .tg_user import TelegramUser
from django.contrib.auth.models import User
from .micro import Product
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}$',
    message="Phone number must be entered in the format: '+998*********'", )



class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
    ]

    customer = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    confirmed_by_user = models.BooleanField(
        default=False,
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.telegram_id} - {self.status}"

    # ✅ Statusni o'zgartirish uchun metod
    def set_status(self, new_status):
        if not self.is_transition_allowed(new_status):
            raise ValueError(f"Invalid status transition: {self.status} -> {new_status}")
        self.status = new_status
        self.save()

    # ✅ Status transition tekshirish
    def is_transition_allowed(self, new_status):
        allowed_transitions = {
            self.PENDING: [self.PROCESSING, self.CANCELED],
            self.PROCESSING: [self.SHIPPED, self.CANCELED],
            self.SHIPPED: [self.DELIVERED, self.CANCELED],
            self.DELIVERED: [],
            self.CANCELED: [],
        }
        return new_status in allowed_transitions.get(self.status, [])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot final price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
