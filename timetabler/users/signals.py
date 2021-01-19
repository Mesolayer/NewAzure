from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from engine.models import UserData

@receiver(post_save, sender=User)
def create_user_data(sender,instance,created,**kwargs):
    #when a new user is registered, create an UserData object
    if created:
        UserData.objects.create(user=instance,name='it works',time_studied = 0, tasks_completed = 0)


@receiver(post_save, sender=User)
def save_user_data(sender,instance,**kwargs):
    instance.userdata.save()
