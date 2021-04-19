from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerProfile(models.Model):
    customer = models.OneToOneField(User, on_delete=CASCADE, related_name='customer_profile')
    name = models.CharField(max_length=254, null=False, blank=False, default="Full name")
    default_address_1 = models.CharField(max_length=80, null=False, blank=False)
    default_address_2 =  models.CharField(max_length=80, null=False, blank=False)
    default_city = models.CharField(max_length=12, null=False, blank=False, default='Dublin')
    default_postcode = models.CharField(max_length=8, null=True, blank=True)
    default_phone_number = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.customer.username


@receiver(post_save, sender=User)
def create_or_update_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(customer=instance)
    instance.customer_profile.save()
