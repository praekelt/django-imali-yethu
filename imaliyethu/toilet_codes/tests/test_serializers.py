""" Tests for toilet code serializers. """

from django.test import TestCase

from imaliyethu.toilet_codes.serializers import ToiletCodeSerializer

from .helpers import create_code, serialize_code, canonicalize_code


class ToiletCodeSerializerTests(TestCase):
    def test_serialize(self):
        code = create_code("TM1234", lat=12.0, lon=-13.0)
        serializer = ToiletCodeSerializer(code)
        self.assertEqual(
            canonicalize_code(serializer.data), serialize_code(code))

    def test_deserialize(self):
        code = create_code("TM1234", lat=-1.0, lon=5.0)
        data = serialize_code(code)
        serializer = ToiletCodeSerializer(data=data)
        serializer.is_valid()
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.object.pk, None)
        self.assertEqual(serializer.object.code, code.code)
