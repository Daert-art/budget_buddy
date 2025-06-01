from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from apps.core.models import Account
import os

User = get_user_model()

# Создание дефолтного аккаунта при создании User
@receiver(post_save, sender=User)
def create_default_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(
            user=instance,
            name=f"Гаманець {instance.username}",
            currency='UAH'
        )

# Удаление старого файла при изменении аватара
@receiver(pre_save, sender=Account)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # Новый объект — нечего удалять

    try:
        old_instance = Account.objects.get(pk=instance.pk)
    except Account.DoesNotExist:
        return  # Объект не найден

    old_file = old_instance.image
    new_file = instance.image

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            try:
                os.remove(old_file.path)
                print(f"[signals] Deleted old avatar: {old_file.path}")
            except Exception as e:
                print(f"[signals] Error deleting old avatar: {e}")

# Удаление файла при удалении Account
@receiver(post_delete, sender=Account)
def delete_account_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            try:
                os.remove(instance.image.path)
                print(f"[signals] Deleted avatar on Account delete: {instance.image.path}")
            except Exception as e:
                print(f"[signals] Error deleting avatar on Account delete: {e}")
