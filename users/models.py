from django.db import models
from django.contrib.auth import models as auth_models
from .constants.interests import INTEREST_CATEGORY_CHOICES, INTEREST_TYPE_CHOICES


class Interest(models.Model):
    type = models.CharField(max_length=50, choices=INTEREST_TYPE_CHOICES)
    category = models.CharField(max_length=50, choices=INTEREST_CATEGORY_CHOICES)

    def __str__(self):
        return '{} - {}'.format(self.get_type_display(), self.get_category_display())


class RendezVousUser(auth_models.User):
    date_of_birth = models.DateField()
    interests = models.ManyToManyField(Interest)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
