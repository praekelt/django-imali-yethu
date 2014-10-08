""" Tests for toilet code models. """

from django.test import TestCase

from imaliyethu.toilet_codes.models import ToiletCode


class ToiletCodeTests(TestCase):
    def test_unicode(self):
        code = ToiletCode.objects.create(
            code="TM123", lat=12.0, lon=13.0)
        self.assertEqual(unicode(code), u"TM123")
