import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from menu.models import MenuItem


# Why pre_delete instead of post_delete
# Since the model is deleted in post_delete, Django will delete the database entry first
# Using pre_delete ensures that the file path is still accessible.
@receiver(pre_delete, sender=MenuItem)
def delete_menu_item_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.exists(image_path):
            os.remove(image_path)
