from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Creates a model for the user's key info to be stored in
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_trainer_code = models.CharField(max_length=20,
                                            null=False, blank=False,
                                            default='XXX-XXXX-XXX')
    default_email = models.CharField(max_length=20,
                                     null=False, blank=False,
                                     default='xx@gmail.com')
    subscription = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):

    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
