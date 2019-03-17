from django.test import TestCase
from django.urls import reverse
from users.models import Interest, User, Profile
from users.constants.interests import (
    INTEREST_CATEGORY_ATTRACTIONS, INTEREST_AMUSEMENT_PARK, INTEREST_AQUARIUM, INTEREST_ART_GALLERY
)


class InterestTestCase(TestCase):
    """Test case for the Interest model"""

    def test_interest_as_str(self):
        """Test the __str__ method"""
        aquarium_interest = Interest.objects.create(type=INTEREST_AQUARIUM, category=INTEREST_CATEGORY_ATTRACTIONS)
        self.assertEqual(
            str(aquarium_interest),
            f'{aquarium_interest.get_type_display()} // {aquarium_interest.get_category_display().upper()}'
        )


class UserTestCase(TestCase):

    user_credentials = {
        'username': 'user',
        'email': 'user@rendezvous.com',
        'password': 'password',
        'first_name': 'user_first',
        'last_name': 'user_last',
    }
    superuser_credentials = {
        'username': 'superuser',
        'email': 'superuser@rendezvous.com',
        'password': 'password',
        'first_name': 'superuser_first',
        'last_name': 'superuser_last',
    }

    def setUp(self):
        """
        Creates a user and superuser for testing.
        This will be run before each test case.
        """
        self.user = User.objects.create_user(**self.user_credentials)
        self.superuser = User.objects.create_superuser(**self.superuser_credentials)

    def tearDown(self):
        """
        Deletes user and superuser.
        This will be run after each test case
        """
        del self.user
        del self.superuser

    def test_user_as_str(self):
        """Test the __str__ method"""
        user = self.user
        self.assertEqual(str(user), user.username)

    def _test_user_profile_exists(self, user):
        """Private method to test that user profile exists"""
        user_profile = Profile.objects.filter(user=user)
        self.assertEqual(user_profile.exists(), True)

    def _test_user_profile_is_empty(self, user):
        """Private method to test that user profile is empty"""
        user_profile = Profile.objects.get(user=user)
        self.assertEqual(user_profile.interests.exists(), False)

    def test_user_creation_creates_empty_profile(self):
        """Check that creating a user automatically creates an empty user profile for them"""
        user = self.user
        self._test_user_profile_exists(user)
        self._test_user_profile_is_empty(user)

    def test_superuser_creation_creates_empty_profile(self):
        """Check that creating a superuser automatically creates an empty user profile for them"""
        superuser = self.superuser
        self._test_user_profile_exists(superuser)
        self._test_user_profile_is_empty(superuser)


class ProfileTestCase(TestCase):

    user_with_interests_credentials = {
        'username': 'user',
        'email': 'user@rendezvous.com',
        'password': 'password',
        'first_name': 'user_first',
        'last_name': 'user_last',
    }
    user_without_interests_credentials = {
        'username': 'user_no_int',
        'email': 'user_no_int@rendezvous.com',
        'password': 'password',
        'first_name': 'user_first',
        'last_name': 'user_last',
    }

    def setUp(self):
        """Create user profile attached to a user and a few interests"""
        user_with_interests = User.objects.create_user(**self.user_with_interests_credentials)
        user_without_interests = User.objects.create_user(**self.user_without_interests_credentials)

        user_with_interests_profile = Profile.objects.get(user=user_with_interests)
        user_without_interests_profile = Profile.objects.get(user=user_without_interests)

        aquarium_interest = Interest.objects.create(
            type=INTEREST_AQUARIUM, category=INTEREST_CATEGORY_ATTRACTIONS
        )
        art_gallery_interest = Interest.objects.create(
            type=INTEREST_ART_GALLERY, category=INTEREST_CATEGORY_ATTRACTIONS
        )
        amusement_park_interest = Interest.objects.create(
            type=INTEREST_AMUSEMENT_PARK, category=INTEREST_CATEGORY_ATTRACTIONS
        )
        user_with_interests_profile.interests.add(aquarium_interest, art_gallery_interest, amusement_park_interest)

        self.profile_with_interests = user_with_interests_profile
        self.profile_without_interests = user_without_interests_profile
        self.aquarium_interest = aquarium_interest
        self.art_gallery_interest = art_gallery_interest
        self.amusement_park_interest = amusement_park_interest

    def tearDown(self):
        del self.profile_with_interests
        del self.profile_without_interests
        del self.aquarium_interest
        del self.art_gallery_interest
        del self.amusement_park_interest

    def test_profile_as_str(self):
        """Test the __str__ method"""
        self.assertEqual(
            str(self.profile_with_interests),
            f'{str(self.aquarium_interest)}, {str(self.art_gallery_interest)}, {str(self.amusement_park_interest)}'
        )

    def test_get_interests_as_json_without_interests(self):
        """Test the get_interest_as_json method for user without interests"""
        profile = self.profile_without_interests
        self.assertEqual(profile.get_interests_as_json(), '[]')

    def test_get_interests_as_json_with_interests(self):
        """Test the get_interest_as_json method for user with interests"""
        profile = self.profile_with_interests
        self.assertEqual(
            profile.get_interests_as_json(),
            f'["{self.aquarium_interest.type}", "{self.art_gallery_interest.type}", '
            f'"{self.amusement_park_interest.type}"]'
        )

    def test_get_absolute_url(self):
        profile = self.profile_with_interests
        self.assertEqual(profile.get_absolute_url(), reverse('users:profile', kwargs={'id': profile.user.id}))
