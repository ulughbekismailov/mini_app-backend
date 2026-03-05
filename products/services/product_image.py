from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Max

from products.models import Product, ProductImage


MAX_IMAGES_PER_PRODUCT = 5


@transaction.atomic
def add_images(product, images):
    """
    Race-condition safe image upload.
    """

    if not images:
        raise ValidationError("No images provided.")

    # 🔒 Lock product row
    product = (
        Product.objects
        .select_for_update()
        .get(pk=product.pk)
    )

    existing_count = product.images.count()
    new_count = len(images)

    if existing_count + new_count > MAX_IMAGES_PER_PRODUCT:
        raise ValidationError(
            f"Maximum {MAX_IMAGES_PER_PRODUCT} images allowed per product."
        )

    last_order = (
        product.images.aggregate(max_order=Max("order"))["max_order"] or 0
    )

    main_exists = product.images.filter(is_main=True).exists()

    created_images = []

    for index, image_file in enumerate(images):
        is_main = False

        if not main_exists and index == 0:
            is_main = True

        product_image = ProductImage.objects.create(
            product=product,
            image=image_file,
            order=last_order + index + 1,
            is_main=is_main,
        )

        created_images.append(product_image)

    return created_images


@transaction.atomic
def delete_image(image: ProductImage):

    product = (
        Product.objects
        .select_for_update()
        .get(pk=image.product.pk)
    )

    was_main = image.is_main
    image.delete()

    if was_main:
        next_image = (
            product.images
            .order_by("created_at")
            .first()
        )

        if next_image:
            next_image.is_main = True
            next_image.save(update_fields=["is_main"])