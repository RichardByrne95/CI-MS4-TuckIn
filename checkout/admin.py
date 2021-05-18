from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'delivery_cost',
                       'order_total', 'grand_total', 'original_bag',
                       'stripe_payment_id')
    fields = ('order_number', 'date', 'customer_profile', 'full_name', 'email', 'phone_number', 'postcode',
              'address_1', 'address_2', 'delivery_cost', 'delivery_time', 'order_total', 'grand_total',
              'original_bag', 'stripe_payment_id', 'rating',)
    list_display = ('order_number', 'date', 'full_name', 'order_total',
                    'delivery_cost', 'grand_total', 'delivery_time', 'rating',)
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
