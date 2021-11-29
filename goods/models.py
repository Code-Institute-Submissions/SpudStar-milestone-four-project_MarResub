from django.db import models

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
    attack = models.IntegerField(default=1)
    defense = models.IntegerField(default=1)
    hp = models.IntegerField(default=1)
    name = models.CharField(max_length=20)
    sp_attack = models.IntegerField(default=1)
    sp_defense = models.IntegerField(default=1)
    speed = models.IntegerField(default=1)
    generation = models.IntegerField(default=1)
    level = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name