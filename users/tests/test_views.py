from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user
from users.views import RegisterView, ProfileView
from users.models import User, Interest, Profile
from users.constants.interests import (
    INTEREST_CATEGORY_ATTRACTIONS, INTEREST_AQUARIUM, INTEREST_ART_GALLERY
)


class RegisterViewTestCase(TestCase):
    """Test case for the register view"""

    url = reverse('users:register')
    view_class = RegisterView
    template_name = RegisterView.template_name
    user_credentials = {
        'username': 'user',
        'email': 'user@rendezvous.com',
        'password': 'password',
        'first_name': 'user_first',
        'last_name': 'user_last',
    }

    def test_get_with_user(self):
        """Tests accessing the register view without logging in"""
        # Create user and log them in
        User.objects.create_user(**self.user_credentials)
        user_credentials = self.user_credentials
        successful_login = self.client.login(
            username=user_credentials['username'],
            password=user_credentials['password'],
        )
        self.assertTrue(successful_login)

        if successful_login:
            # User should be redirected to the mapper page
            response = self.client.get(self.url)
            self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['location'], reverse('mapper:index'))

    def test_get_with_no_user(self):
        """Tests accessing the register view without logging in"""
        response = self.client.get(self.url)
        # Check that request was handled by the correct view and used the correct template
        self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
        self.assertIn(self.template_name, [template.name for template in response.templates])

        # Check the request was successful and rendered with an empty form
        self.assertEqual(response.status_code, 200)
        form = response.context['user_form']
        self.assertFalse(form.is_bound)

    def test_post_with_valid_form(self):
        client = self.client
        user_credentials = self.user_credentials
        response = client.post(self.url, user_credentials)

        # Check correct view handled the request and redirected to user profile
        self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
        self.assertEqual(response.status_code, 302)

        # Check that request created a new user, logged them in and redirected to the correct user's profile
        new_user = User.objects.get(username=user_credentials['username'])
        # Somewhat of a hack as get_user() should be passed a request which has a session attribute
        # works because our client also has a sessions attribute
        logged_in_user = get_user(client)

        self.assertEqual(logged_in_user, new_user)
        self.assertEqual(response['location'], reverse('users:profile', kwargs={'id': new_user.id}))

    def test_post_with_already_created_user(self):
        client = self.client
        user_credentials = self.user_credentials
        # Create user before trying to register with the same user details
        User.objects.create_user(**user_credentials)
        response = client.post(self.url, user_credentials)

        # Check correct view handled the request and redirected to user profile
        self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
        self.assertEqual(response.status_code, 200)

        # Checks the response redraws the page with same template and a bound form
        self.assertIn(self.template_name, [template.name for template in response.templates])
        form = response.context['user_form']
        self.assertTrue(form.is_bound)

        # Ensure that no user was logged in due to invalid form data
        user = get_user(client)
        self.assertFalse(user.is_authenticated)


class ProfileViewTestCase(TestCase):
    """Test case for the profile view"""

    view_class = ProfileView
    template_name = ProfileView.template_name
    success_message = ProfileView.success_message
    user_credentials = {
        'username': 'user',
        'email': 'user@rendezvous.com',
        'password': 'password',
        'first_name': 'user_first',
        'last_name': 'user_last',
    }

    def setUp(self):
        """Creates user and sets his profile url before each test"""
        # Create user and add interest to it
        user = User.objects.create_user(**self.user_credentials)
        aquarium_interest = Interest.objects.create(
            type=INTEREST_AQUARIUM, category=INTEREST_CATEGORY_ATTRACTIONS
        )
        art_gallery_interest = Interest.objects.create(
            type=INTEREST_ART_GALLERY, category=INTEREST_CATEGORY_ATTRACTIONS
        )
        user.profile.interests.add(aquarium_interest, art_gallery_interest)
        self.user = user
        self.aquarium_interest = aquarium_interest
        self.art_gallery_interest = art_gallery_interest
        self.url = reverse('users:profile', kwargs={'id': self.user.id})

    def tearDown(self):
        """Deletes instance variables after each test"""
        del self.user
        del self.aquarium_interest
        del self.art_gallery_interest
        del self.url

    def test_get_with_no_user(self):
        """Test accessing a user profile with no logged-in user"""
        url = self.url
        response = self.client.get(url)
        # Test that view redirects user to the login url with next query parameter set
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'{reverse("login")}?next={url}')

    def test_get_same_user_profile(self):
        """Test logged in user accessing his own profile"""
        client = self.client
        user_credentials = self.user_credentials
        # Log in a user and check it was successful
        successful_login = client.login(
            username=user_credentials['username'],
            password=user_credentials['password'],
        )
        self.assertTrue(successful_login)

        if successful_login:
            response = client.get(self.url)

            # Check request was handled by correct function and was successful
            self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
            self.assertEqual(response.status_code, 200)

            # Check correct template was used for rendering and given a form with the user data in it
            self.assertIn(self.template_name, [template.name for template in response.templates])
            form = response.context['profile_form']
            self.assertEqual(form['interests'].value(), [interest.id for interest in self.user.profile.interests.all()])

    def test_get_different_user_profile(self):
        """Test logged in user accessing someone else's profile"""
        client = self.client
        user_credentials = self.user_credentials

        # Create second user
        second_user_credentials = user_credentials.copy()
        second_user_credentials['username'] = 'user2'
        second_user = User.objects.create_user(**second_user_credentials)

        # Log in as initial user and check it was successful
        successful_login = client.login(
            username=user_credentials['username'],
            password=user_credentials['password'],
        )
        self.assertTrue(successful_login)

        if successful_login:
            # Try to access second user's profile
            second_user_profile_url = reverse('users:profile', kwargs={'id': second_user.id})
            response = client.get(second_user_profile_url)

            # Check request was handled by correct view and was redirected to correct url
            self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['location'], f'{reverse("login")}?next={second_user_profile_url}')

    def test_get_non_existent_user_profile(self):
        """Test logged in user accessing a non-existent user's profile"""
        client = self.client
        user_credentials = self.user_credentials
        # Log in user and check it was successful
        successful_login = client.login(
            username=user_credentials['username'],
            password=user_credentials['password'],
        )
        self.assertTrue(successful_login)

        if successful_login:
            # Try to access a user's profile which does not exist
            non_existent_user_profile_url = reverse('users:profile', kwargs={'id': self.user.id + 1})
            response = client.get(non_existent_user_profile_url)

            # Check request was handled by correct view and was redirected to correct url
            self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
            self.assertEqual(response.status_code, 404)

    def test_post_with_valid_form(self):
        """Test updating profile with valid form"""
        client = self.client
        url = self.url
        user_credentials = self.user_credentials
        # Log in as user and check it was successful
        successful_login = client.login(
            username=user_credentials['username'],
            password=user_credentials['password'],
        )
        self.assertTrue(successful_login)

        if successful_login:
            response = client.post(url, {'interests': (self.aquarium_interest.id, self.art_gallery_interest.id)})

            # Check request was handled by correct view and redirected to correct url
            self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['location'], url)

            # Check that success message was sent with successful request
            self.assertIn(self.success_message, client.cookies['messages'].value)

    def test_post_with_invalid_form(self):
        """Test updating profile with invalid form"""
        client = self.client
        url = self.url
        user_credentials = self.user_credentials
        # Log in as user and check it was successful
        successful_login = client.login(
            username=user_credentials['username'],
            password=user_credentials['password'],
        )
        self.assertTrue(successful_login)

        if successful_login:
            response = client.post(url, {'interests': ("wrong", "type")})

            # Check correct view handled the request
            self.assertEqual(response.resolver_match.func.__name__, self.view_class.as_view().__name__)
            self.assertEqual(response.status_code, 200)

            # Checks the response redraws the page with same template and a bound form
            self.assertIn(self.template_name, [template.name for template in response.templates])
            form = response.context['profile_form']
            self.assertTrue(form.is_bound)
