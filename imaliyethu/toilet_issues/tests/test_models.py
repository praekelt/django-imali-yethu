""" Tests for toilet issue models. """

from django.test import TestCase

from imaliyethu.toilet_issues.models import ToiletIssue, ToiletIssueTranslation


class ToiletIssueTests(TestCase):
    def test_unicode(self):
        issue = ToiletIssue.objects.create(value="broken_seat")
        self.assertEqual(unicode(issue), u"broken_seat")

    def test_add_translation(self):
        issue = ToiletIssue.objects.create(value="broken_seat")
        issue.save()
        issue_en = ToiletIssueTranslation(
            language="en", description="Broken seat")
        issue.translations.add(issue_en)
        [issue_en] = issue.translations.all()
        self.assertEqual(issue_en.issue, issue)
        self.assertEqual(issue_en.language, "en")
        self.assertEqual(issue_en.description, "Broken seat")


class ToiletIssueTranslationTests(TestCase):
    def test_unicode(self):
        issue = ToiletIssue.objects.create(value="broken_lock")
        issue.save()
        issue_xh = ToiletIssueTranslation(
            issue=issue, language="xh", description="Isiphosiso valela")
        self.assertEqual(
            unicode(issue_xh), "Isiphosiso valela (xh, broken_lock)")
