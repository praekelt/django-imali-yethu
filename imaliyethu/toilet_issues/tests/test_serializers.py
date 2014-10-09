""" Tests for toilet issue serializers. """

from django.test import TestCase

from imaliyethu.toilet_issues.serializers import ToiletIssueSerializer

from .helpers import create_issue, serialize_issue


class ToiletIssueSerializerTests(TestCase):
    def test_serialize(self):
        issue = create_issue("leaking_toilet", en="Leaking Toilet", xh="Foo")
        serializer = ToiletIssueSerializer(issue)
        self.assertEqual(serializer.data, serialize_issue(issue))

    def test_deserialize(self):
        issue = create_issue("leaking_toilet", en="Leaking Toilet", xh="Foo")
        data = serialize_issue(issue)
        serializer = ToiletIssueSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.object.pk, None)
        self.assertEqual(serializer.object.value, issue.value)
