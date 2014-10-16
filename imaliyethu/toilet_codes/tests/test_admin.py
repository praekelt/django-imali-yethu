""" Test toilet code admin functions. """

from django.test import TestCase

from imaliyethu.toilet_codes.models import ToiletCode
from imaliyethu.toilet_codes.admin import ToiletCodeAdmin

from .helpers import create_code


class TestToiletCodeAdmin(TestCase):
    def test_export_csv(self):
        create_code("RR1", lat=-1.1, lon=2.2)
        create_code("RR2", lat=3.3, lon=-4.4, section='RR', section_number='1',
                    cluster='2', toilet_type='FT')
        ta = ToiletCodeAdmin(ToiletCode, None)
        csv = ta.get_export_data(ta.formats[0](), ToiletCode.objects.all())
        self.assertEqual(csv, "\r\n".join([
            "Code,Section,Cluster,Number,Type,GPS Latitude,GPS Longitude",
            "RR1,,,,,S1.1,E2.2",
            "RR2,RR,2,1,FT,N3.3,W4.4",
        ]) + "\r\n")
