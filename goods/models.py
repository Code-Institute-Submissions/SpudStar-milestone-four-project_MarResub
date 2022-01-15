from django.db import models

from profiles.models import UserProfile
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=126)
    friendly_name = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Info(models.Model):
    abilities = models.CharField(max_length=30)
    type1 = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    type2 = models.CharField(max_length=20)
    attack = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    hp = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=20)
    sp_attack = models.IntegerField(null=True, blank=True)
    sp_defense = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    generation = models.IntegerField(null=True, blank=True)
    level = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pdex_no = models.IntegerField()
    owner_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='owner_profile')

    def __str__(self):
        return self.name