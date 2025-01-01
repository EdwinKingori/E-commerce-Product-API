from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Customer


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Customer.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    # saving the related customer profile instance whenever the user instance is saved
    if hasattr(instance, 'customer') and not instance.is_superuser:
        instance.customer.save()


@receiver(post_delete, sender=Customer)
def delete_user_profile(sender, instance, **kwargs):
    # deleting the associated user instance when a customer profile is deleted.
    if instance.user:
        instance.customer.delete()
