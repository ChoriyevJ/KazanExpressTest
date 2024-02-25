from django.db.models.signals import post_save
from django.dispatch import receiver

from store.models import Photo


# @receiver(post_save, sender=Photo)
# def get_main_photo(sender, instance, created, **kwargs):
#
#     if created:
#         if instance.is_main:
#             main_photo = instance.image
#             instance.post.main_photo = main_photo
#             instance.post.save()


