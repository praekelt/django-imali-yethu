""" Toilet code views. """

from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from imaliyethu.toilet_codes.models import ToiletCode
from imaliyethu.toilet_codes.serializers import ToiletCodeSerializer


class SearchParams(object):
    """ Holder for search params. """

    def __init__(self, attrs):
        self.errors = []
        self.query = attrs.get('query', None)
        self.threshold = attrs.get('threshold', '0.6')
        self.max_results = attrs.get('max_results', '5')
        self.parse()

    def parse(self):
        if self.query is None:
            self.errors.append("No query specified.")

        try:
            self.threshold = max(float(self.threshold), 0.0)
        except:
            self.errors.append("Value of threshold should be a float.")

        try:
            self.max_results = max(int(self.max_results), 0)
        except:
            self.errors.append("Value of max_results should be an integer.")


class ToiletCodeSearch(APIView):
    """ API endpoint for searching for toilet codes. """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        params = SearchParams(request.GET)
        if params.errors:
            return Response({"error": " ".join(params.errors)},
                            status.HTTP_400_BAD_REQUEST)
        results = ToiletCode.nearest(
            params.query, threshold=params.threshold,
            max_results=params.max_results)
        codes = [r[1] for r in results]
        serializer = ToiletCodeSerializer(codes, many=True)
        return Response(serializer.data)


class ToiletCodeList(ListCreateAPIView):
    """ API endpoint for searching for listing toilet codes. """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = ToiletCode.objects.all()
    serializer_class = ToiletCodeSerializer


class ToiletCodeDetail(RetrieveUpdateDestroyAPIView):
    """ API endpoint for retrieving, updating and deleting a toilet issue. """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = ToiletCode.objects.all()
    serializer_class = ToiletCodeSerializer
