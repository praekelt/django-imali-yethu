""" Tests for toilet code models. """

from django.test import TestCase

from imaliyethu.toilet_codes.models import ToiletCode


class ToiletCodeTests(TestCase):
    def make_codes(self, n=10, template="TM%d"):
        codes = {}
        for i in range(n):
            code = ToiletCode.objects.create(code=template % i, lat=0, lon=0)
            codes[code.code] = code
        return codes

    def test_unicode(self):
        code = ToiletCode.objects.create(
            code="TM123", lat=12.0, lon=13.0)
        self.assertEqual(unicode(code), u"TM123")

    def test_nearest(self):
        codes = self.make_codes()
        self.assertEqual(ToiletCode.nearest("TM1"), [
            (1.0, codes["TM1"]),
            (0.6666666666666666, codes["TM9"]),
            (0.6666666666666666, codes["TM8"]),
            (0.6666666666666666, codes["TM7"]),
            (0.6666666666666666, codes["TM6"]),
        ])

    def test_nearest_max_results(self):
        codes = self.make_codes()
        self.assertEqual(ToiletCode.nearest("TM1", max_results=2), [
            (1.0, codes["TM1"]),
            (0.6666666666666666, codes["TM9"]),
        ])

    def test_nearest_not_enough_results(self):
        codes = self.make_codes(2)
        self.assertEqual(ToiletCode.nearest("TM1", max_results=5), [
            (1.0, codes["TM1"]),
            (0.6666666666666666, codes["TM0"]),
        ])

    def test_nearest_threshold(self):
        codes = self.make_codes(5)
        self.assertEqual(ToiletCode.nearest("TM1", threshold=0.9), [
            (1.0, codes["TM1"]),
        ])
