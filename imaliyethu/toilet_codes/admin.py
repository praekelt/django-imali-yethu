""" Toilet code admin settings. """

from django.contrib import admin

from imaliyethu.toilet_codes.models import ToiletCode


class ToiletCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'lat', 'lon',
    )

    search_fields = (
        'code',
    )


admin.site.register(ToiletCode, ToiletCodeAdmin)
