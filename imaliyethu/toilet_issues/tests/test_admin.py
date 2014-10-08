""" Tests for toilet issue admin interface. """

from django.test import TestCase

from imaliyethu.toilet_issues.admin import display_translation
from imaliyethu.toilet_issues.models import ToiletIssue, ToiletIssueTranslation


class AdminUtilTests(TestCase):
    def test_display_translation_short_description(self):
        f = display_translation("xh", "Xhosa")
        self.assertEqual(f.short_description, "Xhosa")

    def test_display_translation(self):
        f = display_translation("xh", "Xhosa")
        issue = ToiletIssue(value="leaking")
        issue.save()
        issue.translations.add(
            ToiletIssueTranslation(language="xh", description="Ukuvuz"))
        issue.translations.add(
            ToiletIssueTranslation(language="en", description="Leaking"))
        self.assertEqual(f(issue), "Ukuvuz")
