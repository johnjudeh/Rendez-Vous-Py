from django.test import TestCase
from django.core.management import call_command
from users.models import User, Interest
from users.constants.interests import (
    INTEREST_TYPE_TO_CATEGORY_MAPPING
)


class LoadDummyUsersTestCase(TestCase):
    """Test the functionality of the django-admin command load_dummy_users"""

    def setUp(self):
        """Run before each test method"""
        call_command('load_dummy_users', '--silent')

    def _test_user_has_interests(self, user):
        """Tests that user has some interests on their profile"""
        self.assertEqual(user.profile.interests.exists(), True)

    def test_load_dummy_users_command(self):
        """Test the load_dummy_users command successfully loads the required database objects"""
        # Test that interest types are mapped to the right categories
        db_interest_to_cat_mapping = {}
        for interest in Interest.objects.all():
            db_interest_to_cat_mapping[interest.type] = interest.category
        self.assertEqual(db_interest_to_cat_mapping, INTEREST_TYPE_TO_CATEGORY_MAPPING)

        # Test that all dummy users now exist in the database and have some interests
        user = User.objects.get(username='user')
        superuser = User.objects.get(username='superuser')
        self._test_user_has_interests(user)
        self._test_user_has_interests(superuser)
