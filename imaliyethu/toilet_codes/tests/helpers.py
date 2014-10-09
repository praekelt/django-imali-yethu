""" Helpers for toilet code tests. """

from imaliyethu.toilet_codes.models import ToiletCode


def create_code(code, lat=0.0, lon=0.0):
    """ Create a toilet issue with translations. """
    return ToiletCode.objects.create(code=code, lat=lat, lon=lon)


def canonicalize_code(data):
    """ Sort serialized codes for comparison for ease of comparison. """
    if isinstance(data, dict):
        return data
    return [canonicalize_code(c) for c in sorted(data, key=lambda x: x['id'])]


def serialize_code(*args):
    """ Hand-serialize a code for comparison with the real thing. """
    if len(args) == 1:
        code = args[0]
        return canonicalize_code({
            'id': code.pk,
            'code': code.code,
            'lat': code.lat,
            'lon': code.lon,
        })
    else:
        return canonicalize_code([serialize_code(c) for c in args])
