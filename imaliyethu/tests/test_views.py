""" Tests for top-level Imali Yethu views that aren't test elsewhere. """

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from tastypie.test import ResourceTestCase
from tastypie.models import ApiKey


class ApiAuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_login(self):
        response = self.client.get(reverse('rest_framework:login'))
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")


class SnappyViewTests(ResourceTestCase):
    def setUp(self):
        super(SnappyViewTests, self).setUp()
        self.user = get_user_model().objects.create_user(
            username='test', email='test@example.com', password='test_pw')
        self.api_key = ApiKey.objects.create(user=self.user)

    def test_top_level(self):
        auth = self.create_apikey(self.user.username, self.api_key.key)
        response = self.api_client.get(
            '/snappy/api/v1/snappybouncer/useraccount/',
            format='json', authentication=auth)
        self.assertEqual(response.status_code, 200)
        data = self.deserialize(response)
        self.assertEqual(data['objects'], [])
        self.assertEqual(data['meta']['total_count'], 0)


class ApiRootTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page_exists(self):
        response = self.client.get(reverse('api_root'))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin')
        self.assertContains(response, 'api-auth')
        self.assertContains(response, 'toilet_codes')
        self.assertContains(response, 'toilet_issues')
        self.assertContains(response, 'snappy_bouncer')
