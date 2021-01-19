from django.db import models
from django.contrib.auth.models import User


'''
NOTE: Some middleman tables from the ERD have not been included (!!!!) - they are
not necessary thanks to the way Django works! Stuff like the User_Achievement table
can be replaced in Django by a simple "users = models.ManyToManyField(User)" field, for example.
Apart from that, this is *almost* a carbon copy of the ERD, if you're confused.

The way you would get the achievements for a certain user is then:

from django.contrib.auth.models import User
from engine.models import Achievement

user_object = User.objects.get(username='something')
achievements_list = list(Achievement.objects.filter(users=user_object))
'''

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    time_studied = models.IntegerField()
    tasks_completed = models.IntegerField()

    # Defines what is returned when an object of this type is printed
    def __str__(self):
        return self.name.title()



class Achievement(models.Model):
    name = models.CharField(max_length=100)
    hours_required = models.IntegerField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name.title()

class Task(models.Model):
    name = models.CharField(max_length=100)
    start_time_date = models.DateTimeField()
    end_time_date = models.DateTimeField()
    xp_amount_awarded = models.IntegerField()
    is_recurring = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.CharField(max_length=300, blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    reminder_time_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    tasks = models.ManyToManyField(Task)
    #task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return self.name.title()

class PixelArt(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.CharField(max_length=300)
    xp_required = models.IntegerField()
    category = models.CharField(max_length=100)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name.title()
