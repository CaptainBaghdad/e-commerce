from django.contrib import admin

from .models import Item, OrderedItem,Order



admin.site.register(Item)
admin.site.register(OrderedItem)
admin.site.register(Order)