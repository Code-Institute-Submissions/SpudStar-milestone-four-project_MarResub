import uuid

from django.db import models
from django.conf import settings

from goods.models import Info

# Create your models here.
class Order(models.Model):

    order_number = models.CharField(max_length=16, null=False, editable=False)
    full_name = models.CharField(max_length=64, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    user_trainer_code = models.CharField(max_length=255, null=False, blank=False)
    total_requests = models.IntegerField(max_length=16, null=False, default=0)
    date = models.DateTimeField(auto_now_add=True)

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name="lineitems")
    