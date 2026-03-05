from django.db import models
from rest_framework import serializers
from django.utils import timezone

from products.models import Product, Category
from .product_image import ProductImageReadSerializer




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    new_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    images = ProductImageReadSerializer(many=True, read_only=True)
    main_image = serializers.SerializerMethodField()
    is_discount_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'new_price',
            'main_image',
            'images',
            'category',
            'sold_count',
            'discount_percent',
            'discount_start',
            'discount_end',
            'is_active',
            'is_discount_active',
            'description'
        ]

    def validate(self, data):
        discount_percent = data.get('discount_percent')
        discount_start = data.get('discount_start')
        discount_end = data.get('discount_end')

        if discount_percent is not None:
            if not (1 <= discount_percent <= 100):
                raise serializers.ValidationError({
                    'discount_percent': 'Chegirma foizi 1 dan 100 gacha bo\'lishi kerak'
                })

            if not discount_start or not discount_end:
                raise serializers.ValidationError({
                    'discount': 'Chegirma boshlanish va tugash vaqtlari majburiy'
                })

            if discount_start >= discount_end:
                raise serializers.ValidationError({
                    'discount_end': 'Tugash vaqti boshlanish vaqtidan keyin bo\'lishi kerak'
                })

            if discount_start < timezone.now():
                raise serializers.ValidationError({
                    'discount_start': 'Boshlanish vaqti kelajakda bo\'lishi kerak'
                })

        elif discount_start or discount_end:
            raise serializers.ValidationError({
                'discount_percent': 'Chegirma foizi ham berilishi kerak'
            })

        return data

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Narx 0 dan katta bo\'lishi kerak')
        return value

    def get_main_image(self, obj):
        main = obj.images.filter(is_main=True).first()
        if main:
            request = self.context.get('request')
            url = main.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_new_price(self, obj):
        return obj.get_final_price()