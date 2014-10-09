""" Tests for toilet issue views. """

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from imaliyethu.toilet_issues.models import ToiletIssue, ToiletIssueTranslation


def create_issue(value, **translations):
    issue = ToiletIssue(value=value)
    issue.save()
    for language, description in translations.items():
        issue.translations.add(
            ToiletIssueTranslation(language=language, description=description))
    return issue


class ApiListViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_CONTENT_TYPE="application/json")

    def test_list_issues_json(self):
        create_issue("broken_toilet", en="Broken Toilet", xh="Foo")
        create_issue("leaking_toilet", en="Leaking Toilet", xh="Bar")
        response = self.client.get(reverse('toilet_issues_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                'id': 1, 'value': u'broken_toilet', 'translations': [
                    {'id': 1, 'issue': 1, 'language': u'xh',
                     'description': u'Foo'},
                    {'id': 2, 'issue': 1, 'language': u'en',
                     'description': u'Broken Toilet'},
                ]
            }, {
                'id': 2, 'value': u'leaking_toilet', 'translations': [
                    {'id': 3, 'issue': 2, 'language': u'xh',
                     'description': u'Bar'},
                    {u'id': 4, 'issue': 2, 'language': u'en',
                     'description': u'Leaking Toilet'},
                ]
            },
        ])


class ApiDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_CONTENT_TYPE="application/json")

    def test_get_issue_json(self):
        issue = create_issue("broken_toilet", en="Broken Toilet", xh="Foo")
        response = self.client.get(
            reverse('toilet_issues_detail', kwargs={'pk': issue.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'id': 1,
            'value': u'broken_toilet',
            'translations': [
                {'id': 1, 'issue': 1, 'language': u'xh',
                 'description': u'Foo'},
                {'id': 2, 'issue': 1, 'language': u'en',
                 'description': u'Broken Toilet'},
            ],
        })
