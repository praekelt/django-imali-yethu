""" Toilet code admin settings. """

from django.contrib import admin

from import_export.admin import ImportExportMixin

from imaliyethu.toilet_codes.models import ToiletCode
from imaliyethu.toilet_codes.csv_models import ToiletCodeResource


class ToiletCodeAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ToiletCodeResource

    list_display = (
        'code', 'lat', 'lon',
    )

    search_fields = (
        'code',
    )


admin.site.register(ToiletCode, ToiletCodeAdmin)
