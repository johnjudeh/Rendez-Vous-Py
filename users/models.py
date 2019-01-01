from django.db import models
from django.contrib.auth.models import AbstractUser
from .constants.interests import INTEREST_CATEGORY_CHOICES, INTEREST_TYPE_CHOICES
import json


class Interest(models.Model):
    type = models.CharField(max_length=50, choices=INTEREST_TYPE_CHOICES, unique=True)
    category = models.CharField(max_length=50, choices=INTEREST_CATEGORY_CHOICES)

    def __str__(self):
        return '{} - {}'.format(self.get_type_display(), self.get_category_display())


class User(AbstractUser):

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    interests = models.ManyToManyField(Interest)

    def get_interests_as_json(self):
        interest_list = []
        for interest in self.interests.all():
            interest_list.append(interest.type)
        return json.dumps(interest_list)

    def _get_interests_str(self):
        interests_sentence = ''
        for interest in self.interests.all():
            interests_sentence += f'{interest}, '
        interests_sentence = interests_sentence[:-2]
        return interests_sentence

    def __str__(self):
        return self._get_interests_str()