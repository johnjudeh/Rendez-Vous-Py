from django.db import models
from django.contrib.auth import models as auth_models
from .constants.interests import INTEREST_CATEGORY_CHOICES, INTEREST_TYPE_CHOICES
import json


class Interest(models.Model):
    type = models.CharField(max_length=50, choices=INTEREST_TYPE_CHOICES, unique=True)
    category = models.CharField(max_length=50, choices=INTEREST_CATEGORY_CHOICES)

    def __str__(self):
        return '{} - {}'.format(self.get_type_display(), self.get_category_display())


# TODO: This should be split up into a User & UserProfile class according to file:///Users/John/Documents/3.SkillsDev/Computing/Python/Django/django/docs/_build/html/topics/auth/customizing.html#extending-the-existing-user-model
# TODO: Write custom user manager as well
class User(auth_models.AbstractUser):
    date_of_birth = models.DateField()
    interests = models.ManyToManyField(Interest)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_interests_as_json(self):
        interest_list = []
        for interest in self.interests.all():
            interest_list.append(interest.type)
        return json.dumps(interest_list)