from django.db import models

from profiles.models import UserProfile


# Holds all 18 possible pokemon types, plus a 19th entry to allow
# for a lack of a second type
class Category(models.Model):
    name = models.CharField(max_length=126)
    friendly_name = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


"""
 Holds all the pokemons data, uses foreign keys to link the pokemons
 types to the relevant category, as well as a foreign key for the
 owner of the pokemon
"""


class Info(models.Model):
    name = models.CharField(max_length=20)
    level = models.IntegerField(null=True, blank=True)
    pdex_no = models.IntegerField()
    generation = models.IntegerField(null=True, blank=True)
    # Abilities not displayed anywhere due to the odd formatting it in the
    # database I used, kept in as it is still a useful feature that could
    # be implemented in the future
    abilities = models.CharField(max_length=100)

    type1 = models.ForeignKey('Category', null=True, blank=True, 
                              on_delete=models.SET_NULL)
    type2 = models.ForeignKey('Category', null=True, blank=True, 
                              on_delete=models.SET_NULL, related_name='typ2')

    hp = models.IntegerField(null=True, blank=True)
    attack = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    sp_attack = models.IntegerField(null=True, blank=True)
    sp_defense = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)

    # Price was intended to be used but ran out of time, kept as a possible
    # Future implementation as mentioned in readme
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    owner_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                      null=True, blank=True,
                                      related_name='owner_profile')

    def __str__(self):
        return self.name
