""" Test toilet code admin functions. """

import os
import tempfile

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

from imaliyethu.toilet_codes.models import ToiletCode
from imaliyethu.toilet_codes.admin import ToiletCodeAdmin

from .helpers import create_code


class TestToiletCodeAdmin(TestCase):
    def setUp(self):
        self.code_admin = ToiletCodeAdmin(ToiletCode, None)
        self.client = Client()
        self.export_formats = self.gather_formats(
            self.code_admin.get_export_formats())
        self.import_formats = self.gather_formats(
            self.code_admin.get_export_formats())
        self.user = get_user_model().objects.create_superuser(
            username='test', email='test@example.com', password='test_pw')
        self._tmp_csv = []

    def tearDown(self):
        for f in self._tmp_csv:
            os.remove(f)

    def gather_formats(self, formats):
        format_dict = {}
        for idx, cls in enumerate(formats):
            f = cls()
            f.idx = idx
            format_dict[f.get_title()] = f
        return format_dict

    def make_csv(self, lines):
        with tempfile.NamedTemporaryFile(delete=False) as csv_file:
            csv_file.write("\r\n".join(lines))
            csv_file.write("\r\n")
        self._tmp_csv.append(csv_file.name)
        return os.path.basename(csv_file.name)

    def test_export_csv(self):
        create_code("RR1", lat=-1.1, lon=2.2)
        create_code("RR2", lat=3.3, lon=-4.4, section='RR', section_number='1',
                    cluster='2', toilet_type='FT')
        csv_format = self.export_formats['csv']
        csv = self.code_admin.get_export_data(
            csv_format, ToiletCode.objects.all())
        self.assertEqual(csv, "\r\n".join([
            "Code,Section,Cluster,Number,Type,GPS Latitude,GPS Longitude",
            "RR1,,,,,S1.1,E2.2",
            "RR2,RR,2,1,FT,N3.3,W4.4",
        ]) + "\r\n")

    def do_import(self, lines):
        csv_name = self.make_csv(lines)
        csv_format = self.import_formats['csv']
        self.client.login(username='test', password='test_pw')
        response = self.client.post(
            reverse('admin:toilet_codes_toiletcode_process_import'),
            data={
                'input_format': str(csv_format.idx),
                'import_file_name': csv_name,
            }
        )
        self.assertRedirects(response, '/admin/toilet_codes/toiletcode/')

    def test_import_csv(self):
        self.do_import([
            "Code,Section,Cluster,Number,Type,GPS Latitude,GPS Longitude",
            "RR1,,,,,S1.1,E2.2",
            "RR2,RR,2,1,FT,N3.3,W4.4",
        ])

        [code1, code2] = ToiletCode.objects.all().order_by('code')

        self.assertEqual(code1.code, "RR1")
        self.assertEqual(code1.section, "")
        self.assertEqual(code1.cluster, "")
        self.assertEqual(code1.section_number, "")
        self.assertEqual(code1.toilet_type, "")
        self.assertEqual(code1.lat, -1.1)
        self.assertEqual(code1.lon, 2.2)

        self.assertEqual(code2.code, "RR2")
        self.assertEqual(code2.section, "RR")
        self.assertEqual(code2.cluster, "2")
        self.assertEqual(code2.section_number, "1")
        self.assertEqual(code2.toilet_type, "FT")
        self.assertEqual(code2.lat, 3.3)
        self.assertEqual(code2.lon, -4.4)

    def test_import_csv_update(self):
        create_code("RR2")
        self.do_import([
            "Code,Section,Cluster,Number,Type,GPS Latitude,GPS Longitude",
            "RR2,RR,2,1,FT,N3.3,W4.4",
        ])

        [code] = ToiletCode.objects.all().order_by('code')

        self.assertEqual(code.code, "RR2")
        self.assertEqual(code.section, "RR")
        self.assertEqual(code.cluster, "2")
        self.assertEqual(code.section_number, "1")
        self.assertEqual(code.toilet_type, "FT")
        self.assertEqual(code.lat, 3.3)
        self.assertEqual(code.lon, -4.4)
