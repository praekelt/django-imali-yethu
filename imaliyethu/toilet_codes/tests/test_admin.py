""" Test toilet code admin functions. """

from django.test import TestCase

from imaliyethu.toilet_codes.models import ToiletCode
from imaliyethu.toilet_codes.admin import ToiletCodeAdmin

from .helpers import create_code


class TestToiletCodeAdmin(TestCase):
    def test_export_csv(self):
        create_code("RR1", lat=-1.0, lon=2.0)
        create_code("RR2", lat=3.0, lon=-4.0, section='RR', section_number='1',
                    cluster='2', toilet_type='FT')
        ta = ToiletCodeAdmin(ToiletCode, None)
        csv = ta.get_export_data(ta.formats[0](), ToiletCode.objects.all())
        self.assertEqual(csv, "\r\n".join([
            "Code,Section,Cluster,Number,Type,GPS Latitude,GPS Longitude",
            "RR1,,,,,-1.0,2.0",
            "RR2,RR,2,1,FT,3.0,-4.0",
        ]) + "\r\n")
