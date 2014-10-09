""" Tests for toilet code views. """

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from .helpers import create_code, serialize_code, canonicalize_code


class ApiSearchViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_CONTENT_TYPE="application/json")
        self.codes = dict(
            (i, create_code("TMN123%d" % i))
            for i in range(5))

    def test_simple_search(self):
        response = self.client.get(
            reverse('toilet_codes_search') + '?query=TM123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [canonicalize_code(c) for c in response.data],
            [serialize_code(self.codes[i]) for i in (4, 3, 2, 1, 0)],
        )

    def test_max_results(self):
        response = self.client.get(
            reverse('toilet_codes_search') + '?query=TM123&max_results=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [canonicalize_code(c) for c in response.data],
            [serialize_code(self.codes[i]) for i in (4, 3, 2)],
        )

    def test_threshold(self):
        response = self.client.get(
            reverse('toilet_codes_search') + '?query=TM1233&threshold=0.9')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [canonicalize_code(c) for c in response.data],
            [serialize_code(self.codes[3])],
        )


class ApiListViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_CONTENT_TYPE="application/json")

    def test_list_issues_json(self):
        code_1 = create_code("TM123", lat=12.0, lon=-5.0)
        code_2 = create_code("TM456")
        response = self.client.get(reverse('toilet_codes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            canonicalize_code(response.data),
            serialize_code(code_1, code_2))


class ApiDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_CONTENT_TYPE="application/json")

    def test_get_issue_json(self):
        code = create_code("TM123", lat=12.0, lon=-1.0)
        response = self.client.get(
            reverse('toilet_codes_detail', kwargs={'pk': code.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            canonicalize_code(response.data), serialize_code(code))
