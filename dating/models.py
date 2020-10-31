import random


from django.db import models
from django.conf import settings

# Create your models here.


def profile_id_generator():
    try_again = True
    prof_number = str(random.randint(100001, 999999))

    while try_again:
        qs_exists= Profile.objects.filter(profile_number=prof_number).exists()
        if not qs_exists:
            try_again = False

    return prof_number


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_number = models.CharField(max_length=10, unique=True, blank=False, null=False, default=profile_id_generator)
    age = models.IntegerField(null=False, blank=False)
    friends = models.ManyToManyField("Profile", blank=True)
    unread_message_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + ' - ' + str(self.id)




