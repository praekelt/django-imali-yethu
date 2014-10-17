""" Import / Export models for toilet codes. """

import math
import re

from import_export import resources
from import_export import fields

from imaliyethu.toilet_codes.models import ToiletCode


class GPSField(fields.Field):
    PATTERN = re.compile(r"""
        ^(?P<direction>[NEWS])
        \s*(?P<int>\d+)?
        ([.,](?P<frac>\d+))?$
    """, re.VERBOSE)

    def __init__(self, gps_type, **kw):
        super(GPSField, self).__init__(**kw)
        self.gps_type = gps_type
        if self.gps_type == 'lat':
            self._pos_dir = 'N'
            self._neg_dir = 'S'
        elif self.gps_type == 'lon':
            self._pos_dir = 'E'
            self._neg_dir = 'W'
        else:
            raise ValueError("gps_type must be either lat or lon.")

    def clean(self, data):
        value = data.get(self.column_name)
        if value is None:
            return None
        match = self.PATTERN.match(value.strip())
        if match is None:
            return 0.0
        groups = match.groupdict()
        sign = -1.0 if (groups["direction"] == self._neg_dir) else 1.0
        int_part = groups["int"] or "0"
        frac_part = groups["frac"] or "0"
        return sign * float("%s.%s" % (int_part, frac_part))

    def export(self, obj):
        value = self.get_value(obj)
        if value is None:
            return value
        direction = self._pos_dir if (value >= 0) else self._neg_dir
        # 15 decimal places is the maximum useful precision shared between
        # decimal and IEEE floating point representations
        gps = "%s%.15g" % (direction, math.fabs(value))
        return gps


class ToiletCodeResource(resources.ModelResource):

    code = fields.Field(
        attribute='code', column_name="Code")
    lat = GPSField(
        gps_type='lat', attribute='lat', column_name="GPS Latitude")
    lon = GPSField(
        gps_type='lon', attribute='lon', column_name="GPS Longitude")

    section = fields.Field(
        attribute='section', column_name="Section")
    section_number = fields.Field(
        attribute='section_number', column_name="Number")
    cluster = fields.Field(
        attribute='cluster', column_name="Cluster")
    toilet_type = fields.Field(
        attribute='toilet_type', column_name="Type")

    class Meta:
        model = ToiletCode
        import_id_fields = ('code',)
        export_order = (
            'code', 'section', 'cluster', 'section_number', 'toilet_type',
            'lat', 'lon',
        )
