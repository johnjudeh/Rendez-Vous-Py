from django.test import TestCase
from django.urls import reverse
from ..views import MapperView, MAPS_KEY_LABEL
from users.models import User
import os


# Create your tests here.
class MapperViewTestCase(TestCase):
    """Test case for the MapperView"""

    url = reverse('mapper:index')
    template_name = MapperView.template_name
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

    def _test_basic_response_characteristics(self, response):
        """Test that correct view, template and context were used successfully"""
        # The first assertion looks a little strange because an anonymous function created by
        # an instance of the MapperView class is used to handle the view. This function is
        # therefore different each time you run MapperView.as_view() so we compare the __name__
        # attribute rather than the function directly.
        self.assertEqual(response.resolver_match.func.__name__, MapperView.as_view().__name__)
        self.assertIn(self.template_name, [template.name for template in response.templates])
        self.assertEqual(response.context[MAPS_KEY_LABEL], os.environ[MAPS_KEY_LABEL])
        # Check view responded successfully with a HTML page
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')

    def _test_logged_in_user_response_characteristics(self, response, user):
        """Test the response context has correct user instance in it"""
        self.assertEqual(response.context['user'], user)

    def test_mapper_view_get_without_user(self):
        """Tests a successful GET request to the mapper index page with no user"""
        # The client has persistent state, meaning it holds onto cookies and other
        # pieces of data between requests
        response = self.client.get(self.url)
        self._test_basic_response_characteristics(response)

    def test_mapper_view_get_with_user(self):
        """Tests a successful GET request to the mapper index page with a normal user"""
        user_cred = self.user_credentials
        successful_login = self.client.login(
            username=user_cred['username'],
            password=user_cred['password'],
        )
        self.assertEqual(successful_login, True)

        if successful_login:
            response = self.client.get(self.url)
            self._test_basic_response_characteristics(response)
            self._test_logged_in_user_response_characteristics(response, self.user)

    def test_mapper_view_get_with_superuser(self):
        """Tests a successful GET request to the mapper index page with a super user"""
        superuser_cred = self.superuser_credentials
        successful_login = self.client.login(
            username=superuser_cred['username'],
            password=superuser_cred['password'],
        )
        self.assertEqual(successful_login, True)

        if successful_login:
            response = self.client.get(self.url)
            self._test_basic_response_characteristics(response)
            self._test_logged_in_user_response_characteristics(response, self.superuser)
