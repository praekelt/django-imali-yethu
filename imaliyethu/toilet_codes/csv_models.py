""" Import / Export models for toilet codes. """

from import_export import resources
from import_export import fields

from imaliyethu.toilet_codes.models import ToiletCode


class GPSField(fields.Field):
    def __init__(self, gps_type, **kw):
        super(GPSField, self).__init__(**kw)
        self.gps_type = gps_type

    def clean(self, data):
        return data

    def export(self, obj):
        return super(GPSField, self).export(obj)


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
