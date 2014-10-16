""" Toilet code admin settings. """

from django.contrib import admin

from imaliyethu.toilet_codes.models import ToiletCode


class ToiletCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'section', 'cluster', 'section_number', 'toilet_type',
        'lat', 'lon',
    )

    search_fields = (
        'code', 'section', 'toilet_type',
    )


admin.site.register(ToiletCode, ToiletCodeAdmin)
