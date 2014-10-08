""" Django REST framework serializers for toilet issues. """

from rest_framework import serializers

from imaliyethu.toilet_issues.models import ToiletIssue


class ToiletIssueSerializer(serializers.Serializer):
    pk = serializers.Field()
    value = serializers.CharField(required=True, max_length=1024)

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.value = attrs.get('value', instance.value)
            return instance

        return ToiletIssue(**attrs)
