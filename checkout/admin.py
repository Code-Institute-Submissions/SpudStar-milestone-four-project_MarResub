from django.contrib import admin

# Register your models here.
from .models import Order

class OrderAdmin(admin.ModelAdmin):

    readonly_fields = ('order_number', 'date',)

    fields = ('order_number', 'date', 'email', 'full_name', 'user_trainer_code')

    list_display = ('order_number', 'date', 'full_name',)

    ordering = ('-date',)

admin.site.register(Order, OrderAdmin)