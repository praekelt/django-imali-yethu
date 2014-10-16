from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^toilet_issues/', include('imaliyethu.toilet_issues.urls')),
    url(r'^toilet_codes/', include('imaliyethu.toilet_codes.urls')),
    url(r'^api-auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    # TastyPie breaks if a namespace is set. See
    # https://github.com/toastdriven/django-tastypie/issues/24
    url(r'^snappy/', include('snappybouncer.urls')),
)
