""" Toilet issue views. """

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)

from imaliyethu.toilet_issues.models import ToiletIssue
from imaliyethu.toilet_issues.serializers import ToiletIssueSerializer


class ToiletIssueList(ListCreateAPIView):
    """ API endpoint for listing and creating toilet issues. """

    queryset = ToiletIssue.objects.all()
    serializer_class = ToiletIssueSerializer


class ToiletIssueDetail(RetrieveUpdateDestroyAPIView):
    """ API endpoint for retrieving, updating and deleting a toilet issue. """

    queryset = ToiletIssue.objects.all()
    serializer_class = ToiletIssueSerializer
