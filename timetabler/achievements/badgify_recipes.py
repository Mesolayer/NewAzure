from django.contrib.staticfiles.storage import staticfiles_storage
from badgify.recipe import BaseRecipe
import badgify
from engine.models import UserData

#creates a list of badges/achievements that can be awarded
class BeginnerTaskerRecipe(BaseRecipe):
    name = 'Beginner Tasker'
    slug = 'beginner-tasker'
    description = 'You have completed your first task! Congratulations!'


    @property
    def image(self):
        images = 'awards.png'
        return images


    @property
    def user_ids(self):
        return(UserData.objects.filter(tasks_completed__gte=1).values_list('user',flat=True)) #lists the condition required to achieve badge

class NoviceTaskerRecipe(BaseRecipe):
    name = 'Novice Tasker'
    slug = 'novice-tasker'
    description = 'You have completed 10 tasks! Congratulations!'

    @property
    def image(self):
        images = 'awards.png'
        return images

    @property
    def user_ids(self):
        return(UserData.objects.filter(tasks_completed__gte=10).values_list('user',flat=True)) #lists the condition required to achieve badge


class AdvancedTaskerRecipe(BaseRecipe):
    name = 'Advanced Tasker'
    slug = 'advanced-tasker'
    description = 'You have completely 50 tasks! Becoming a veteran!'

    @property
    def image(self):
        images = 'awards.png'
        return images

    @property
    def user_ids(self):
        return(UserData.objects.filter(tasks_completed__gte=50).values_list('user',flat=True)) #lists the condition required to achieve badge

class MasterTaskerRecipe(BaseRecipe):
    name = 'Master Tasker'
    slug = 'master-tasker'
    description = 'You have mastered using tasks! Congrats on completing 100 tasks!'

    @property
    def image(self):
        images = 'awards.png'
        return images

    @property
    def user_ids(self):
        return(UserData.objects.filter(tasks_completed__gte=100).values_list('user',flat=True)) #lists the condition required to achieve badge

class BusyBodyRecipe(BaseRecipe):
    name = 'Busy Body'
    slug = 'busy-body'
    description = 'You have spent 1 hour doing tasks! Get a move on!'

    @property
    def image(self):
        images = 'awards.png'
        return images

    @property
    def user_ids(self):
        return(UserData.objects.filter(time_studied__gte=1).values_list('user',flat=True)) #lists the condition required to achieve badge

class TeachersPetRecipe(BaseRecipe):
    name = 'Teachers Pet'
    slug = 'teachers-pet'
    description = 'You seem to love studying... Congratulations on 10 hours!'

    @property
    def image(self):
        images = 'awards.png'
        return images

    @property
    def user_ids(self):
        return(UserData.objects.filter(time_studied__gte=10).values_list('user',flat=True)) #lists the condition required to achieve badge

#adds the badges to the website
#also need to run python badgify_sync badges when first run, python badgify_sync badges --update when adding new badges
badgify.register(BeginnerTaskerRecipe)
badgify.register(NoviceTaskerRecipe)
badgify.register(AdvancedTaskerRecipe)
badgify.register(MasterTaskerRecipe)
badgify.register(BusyBodyRecipe)
badgify.register(TeachersPetRecipe)
