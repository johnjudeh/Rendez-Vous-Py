from django.core.management.base import BaseCommand, CommandError
from users.models import RendezVousUser, Interest
from users.constants.interests import (
    INTEREST_TYPE_TO_CATEGORY_MAPPING, INTEREST_BAR, INTEREST_RESTAURANT, INTEREST_NIGHT_CLUB
)
from datetime import date

class Command(BaseCommand):
    help = 'Loads dummy users to the database for local testing'

    def _set_up_interest_mapping(self):
        for interest_type, interest_cat in INTEREST_TYPE_TO_CATEGORY_MAPPING.items():
            if Interest.objects.filter(type=interest_type).count() == 0:
                Interest.objects.create(
                    type=interest_type,
                    category=interest_cat,
                )
        self.stdout.write(self.style.SUCCESS('Successfully set up interest category mapping'))

    def _create_user(self, super_user=False):
        username = 'superuser' if super_user else 'user'
        user = RendezVousUser(
            first_name=username,
            username=username,
            email='{}@rendezvous.com'.format(username),
            date_of_birth=date(1990, 1, 1).isoformat(),
            is_staff=(True if super_user else False),
            is_superuser=(True if super_user else False),
        )
        user.set_password('password')
        user.save()
        interest_bar = Interest.objects.get(type=INTEREST_BAR)
        interest_restaurant = Interest.objects.get(type=INTEREST_RESTAURANT)
        interest_night_club = Interest.objects.get(type=INTEREST_NIGHT_CLUB)
        user.interests.add(
            interest_bar,
            interest_restaurant,
            interest_night_club,
        )
        self.stdout.write(self.style.SUCCESS('Successfully created {} account'.format(username)))

    def handle(self, *args, **options):
        self._set_up_interest_mapping()
        self._create_user(super_user=True)
        self._create_user(super_user=False)
