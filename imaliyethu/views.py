from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRoot(APIView):
    """
    API for the Imali Yethu project.
    """
    def get(self, request, format=None):
        return Response({
            'admin': reverse('admin:index', request=request),
            'api-auth': reverse('rest_framework:login', request=request),
            'toilet_codes': reverse('toilet_codes_list', request=request),
            'toilet_issues': reverse('toilet_issues_list', request=request),
            'snappy_bouncer': '%s?format=json' % request.build_absolute_uri(
                reverse(
                    'api_v1/snappybouncer_top_level',
                    kwargs={'api_name': 'v1/snappybouncer'}, request=request)),
            })
