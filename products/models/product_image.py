from django.db import models
from django.core.validators import FileExtensionValidator


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'gif'])]
    )
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['product'],
                condition=models.Q(is_main=True),
                name='unique_main_image_per_product'
            )
        ]
        indexes = [
            models.Index(fields=['product', 'order']),
        ]

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

    @property
    def url(self):
        return self.image.url if self.image else ''