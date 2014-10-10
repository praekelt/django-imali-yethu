""" Django REST framework serializers for toilet codes. """

from rest_framework import serializers

from imaliyethu.toilet_codes.models import ToiletCode


class ToiletCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToiletCode
        fields = (
            'id', 'code', 'lat', 'lon',
            'section', 'section_number', 'cluster',
            'toilet_type',
        )
