""" Toilet code admin settings. """

from django.contrib import admin

from import_export.admin import ImportExportMixin

from imaliyethu.toilet_codes.models import ToiletCode
from imaliyethu.toilet_codes.csv_models import ToiletCodeResource


class ToiletCodeAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ToiletCodeResource

    list_display = (
        'code', 'section', 'cluster', 'section_number', 'toilet_type',
        'lat', 'lon',
    )

    search_fields = (
        'code', 'section', 'toilet_type',
    )


admin.site.register(ToiletCode, ToiletCodeAdmin)
