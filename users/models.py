from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from .constants.interests import INTEREST_CATEGORY_CHOICES, INTEREST_TYPE_CHOICES
import json


class Interest(models.Model):

    type = models.CharField(max_length=50, choices=INTEREST_TYPE_CHOICES, unique=True)
    category = models.CharField(max_length=50, choices=INTEREST_CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.get_type_display()} // {self.get_category_display().upper()}'


class User(AbstractUser):

    def __str__(self):
        return f'{self.username}'


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    interests = models.ManyToManyField(Interest)

    # Methods on models add row-level functionality
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

    def get_absolute_url(self):
        """
        Returns the specific url for a model instance.
        A special purpose object method that is used in the admin app and can
        be used in templates rather than specifically writing it out.
        Try to always define this on your models.
        """
        return reverse('users:profile', args=[self.user.id])