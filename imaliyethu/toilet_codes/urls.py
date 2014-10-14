""" URL patterns for toilet codes. """

from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from imaliyethu.toilet_codes.views import (
    ToiletCodeSearch, ToiletCodeList, ToiletCodeDetail)

urlpatterns = patterns(
    '',
    url(r'^$', ToiletCodeList.as_view(),
        name='toilet_codes_list'),
    url(r'^search$', ToiletCodeSearch.as_view(),
        name='toilet_codes_search'),
    url(r'^(?P<pk>[0-9]+)/$', ToiletCodeDetail.as_view(),
        name='toilet_codes_detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
