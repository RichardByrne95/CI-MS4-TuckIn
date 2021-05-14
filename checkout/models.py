import uuid
from django.db import models
from django.db.models import Sum
from django.db.models.deletion import CASCADE, RESTRICT
from restaurants.models import Restaurant, FoodItem
from profiles.models import CustomerProfile

class Order(models.Model):
    order_number = models.CharField(max_length=16, null=False, editable=False)
    order_restaurant = models.ForeignKey(Restaurant, max_length=128, null=False, blank=False, on_delete=RESTRICT)
    customer_profile = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True, blank=False, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=128, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False, default=0)
    address_1 = models.CharField(max_length=80, null=False, blank=False)
    address_2 = models.CharField(max_length=80, null=True, blank=True)
    city = models.CharField(max_length=6, null=False, blank=False, default='Dublin')
    postcode = models.CharField(max_length=8, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateTimeField(null=True, blank=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.JSONField(null=False, blank=False, default=dict)
    stripe_payment_id = models.CharField(max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        number = uuid.uuid4().hex
        return str(number)[:16]

    def update_total(self):
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.delivery_cost = self.delivery_cost
        self.grand_total = self.delivery_cost + self.order_total
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.order_number

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=CASCADE, related_name='lineitems')
    food_item = models.ForeignKey(FoodItem, null=False, blank=False, on_delete=RESTRICT)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    additional_details = models.CharField(max_length=256, null=True, blank=True)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = self.food_item.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.food_item.friendly_name} on order {self.order.order_number}'
