""" URL patterns for toilet issues. """

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from imaliyethu.toilet_issues.views import ToiletIssueList, ToiletIssueDetail

urlpatterns = patterns(
    '',
    url(r'^$', ToiletIssueList.as_view(),
        name='toilet_issues_list'),
    url(r'^(?P<pk>[0-9]+)/$', ToiletIssueDetail.as_view(),
        name='toilet_issues_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
