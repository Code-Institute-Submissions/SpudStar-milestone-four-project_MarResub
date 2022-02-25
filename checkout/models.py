import uuid

from django.db import models

from goods.models import Info
from profiles.models import UserProfile

# My order model, contains key fields for a trade request


class Order(models.Model):

    # The Order Number to Identify it
    order_number = models.CharField(max_length=100, null=False, editable=False)
    # The name/username associated with the order
    full_name = models.CharField(max_length=64, null=False, blank=False)
    # The email associated with the order
    email = models.EmailField(max_length=50, null=False, blank=False)
    # The trainer code associated with the order
    user_trainer_code = models.CharField(max_length=20,
                                         null=False, blank=False,)
    # The date the order was made
    date = models.DateTimeField(auto_now_add=True)
    # The logged in User associated with the order
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')

    # Logic for generating order number from Boutique Ado
    def _generate_order_number(self):

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):

        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


# Allows each pokemon in a request to be assigned to the same order
class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Info, null=False, blank=False,
                                on_delete=models.CASCADE, default="")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name
