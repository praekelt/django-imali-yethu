""" Tests for toilet code CSV helper. """

from StringIO import StringIO

from django.test import TestCase

from imaliyethu.toilet_codes.toilet_code_csv import ToiletCode
from imaliyethu.toilet_codes.toilet_code_csv import ToiletCodeCsv
from .helpers import create_code


class ToiletCodeCsvTests(TestCase):
    def setUp(self):
        self.tcsv = ToiletCodeCsv()

    def make_file(self, lines, newline="\n"):
        f = StringIO(newline.join(lines))
        return f

    def assert_file_equal(self, f, lines, newline="\r\n"):
        data = newline.join(lines + [''])
        self.assertEqual(f.getvalue(), data)

    def test_read(self):
        csv = self.make_file([
            'Code,Section,Cluster,Number,Type,Condition,"Photo file",'
            '"GPS Latitude","GPS Longitude",Notes',
            'RR001001FT,RR,1,1,FT,Locked,,"S34.01667","E18.66404",',
            'RR001002FT,RR,1,2,FT,Locked,,"S35.01667","E19.66404",',
        ])
        self.tcsv.read_csv(csv)
        [code1, code2] = ToiletCode.objects.all().order_by('code')

        self.assertEqual(code1.code, "RR001001FT")
        self.assertEqual(code1.section, "RR")
        self.assertEqual(code1.cluster, "1")
        self.assertEqual(code1.section_number, "1")
        self.assertEqual(code1.toilet_type, "FT")
        self.assertEqual(code1.lat, float("-34.01667"))
        self.assertEqual(code1.lon, float("18.66404"))

        self.assertEqual(code2.code, "RR001002FT")
        self.assertEqual(code2.section, "RR")
        self.assertEqual(code2.cluster, "1")
        self.assertEqual(code2.section_number, "2")
        self.assertEqual(code2.toilet_type, "FT")
        self.assertEqual(code2.lat, float("-35.01667"))
        self.assertEqual(code2.lon, float("19.66404"))

    def test_read_update(self):
        create_code("RR001001FT")
        csv = self.make_file([
            'Code,Section,Cluster,Number,Type,Condition,"Photo file",'
            '"GPS Latitude","GPS Longitude",Notes',
            'RR001001FT,RR,1,1,FT,Locked,,"S34.01667","E18.66404",',
        ])
        self.tcsv.read_csv(csv)
        [new_code] = ToiletCode.objects.all()

        self.assertEqual(new_code.code, "RR001001FT")
        self.assertEqual(new_code.section, "RR")
        self.assertEqual(new_code.cluster, "1")
        self.assertEqual(new_code.section_number, "1")
        self.assertEqual(new_code.toilet_type, "FT")
        self.assertEqual(new_code.lat, float("-34.01667"))
        self.assertEqual(new_code.lon, float("18.66404"))

    def test_write(self):
        create_code(
            "RR123", lat=-12.1, lon=5.1, section="RR", section_number="12",
            toilet_type="SP", cluster="3")
        f = StringIO()
        self.tcsv.write_csv(f)
        self.assert_file_equal(f, [
            'Code,Section,Cluster,Number,Type,GPS Latitude,GPS Longitude',
            'RR123,RR,3,12,SP,S12.1,E5.1',
        ])
