from django.contrib import admin
from .models import Order, OrderLineItem

# From Boutique Ado
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)

# Referenced Boutique Ado
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total', 'grand_total')
    fields = ('order_number', 'date', 'full_name', 'email', 'phone_number', 'postcode',
              'address_1', 'address_2', 'delivery_cost', 'order_total', 'grand_total',)
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost', 'grand_total',)
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
