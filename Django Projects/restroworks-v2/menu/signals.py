import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from menu.models import MenuItem


@receiver(pre_delete, sender=MenuItem)
def delete_menu_item_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path) and os.path.basename(image_path) != "default.png":
            os.remove(image_path)
