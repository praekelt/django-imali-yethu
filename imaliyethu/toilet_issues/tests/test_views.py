""" Tests for toilet issue views. """

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from .helpers import create_issue, serialize_issue, canonicalize_issue


class ApiListViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_CONTENT_TYPE="application/json")

    def test_list_issues_json(self):
        issue_1 = create_issue("broken_toilet", en="Broken Toilet", xh="Foo")
        issue_2 = create_issue("leaking_toilet", en="Leaking Toilet", xh="Bar")
        response = self.client.get(reverse('toilet_issues_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            canonicalize_issue(response.data),
            serialize_issue(issue_1, issue_2))


class ApiDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_CONTENT_TYPE="application/json")

    def test_get_issue_json(self):
        issue = create_issue("broken_toilet", en="Broken Toilet", xh="Foo")
        response = self.client.get(
            reverse('toilet_issues_detail', kwargs={'pk': issue.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            canonicalize_issue(response.data), serialize_issue(issue))
