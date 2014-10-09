""" Tests for toilet code views. """

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from imaliyethu.toilet_codes.views import SearchParams

from .helpers import create_code, serialize_code, canonicalize_code


class SearchParamsTests(TestCase):
    def test_defaults(self):
        s = SearchParams({'query': 'foo'})
        self.assertEqual(s.errors, [])
        self.assertEqual(s.query, 'foo')
        self.assertEqual(s.threshold, 0.6)
        self.assertEqual(s.max_results, 5)

    def test_no_query(self):
        s = SearchParams({})
        self.assertEqual(s.errors, ["No query specified."])

    def test_non_float_threshold(self):
        s = SearchParams({'query': 'foo', 'threshold': 'b'})
        self.assertEqual(s.errors, ["Value of threshold should be a float."])

    def test_threshold_underflow(self):
        s = SearchParams({'query': 'foo', 'threshold': '-5.0'})
        self.assertEqual(s.errors, [])
        self.assertEqual(s.threshold, 0.0)

    def test_non_integer_max_results(self):
        s = SearchParams({'query': 'foo', 'max_results': 'b'})
        self.assertEqual(
            s.errors, ["Value of max_results should be an integer."])

    def test_max_results_underflow(self):
        s = SearchParams({'query': 'foo', 'max_results': '-3'})
        self.assertEqual(s.errors, [])
        self.assertEqual(s.max_results, 0)


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
