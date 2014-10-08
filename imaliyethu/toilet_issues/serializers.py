""" Django REST framework serializers for toilet issues. """

from rest_framework import serializers

from imaliyethu.toilet_issues.models import ToiletIssue


class ToiletIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToiletIssue
        fields = ('id', 'value', 'translations')
        depth = 1
