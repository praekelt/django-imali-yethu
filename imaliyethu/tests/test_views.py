""" Tests for top-level Imali Yethu views that aren't test elsewhere. """

from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class ApiAuthViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_login(self):
        response = self.client.get(reverse('rest_framework:login'))
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")
