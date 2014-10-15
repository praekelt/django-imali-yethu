""" Toilet issue admin settings. """

from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from imaliyethu.toilet_issues.models import ToiletIssue, ToiletIssueTranslation


class ToiletIssueTranslationInline(admin.TabularInline):
    model = ToiletIssueTranslation
    extra = 1


def display_translation(lang_code, lang_label):
    """ Construct a function for displaying a column of translations. """
    def display(issue):
        translations = issue.translations.filter(language=lang_code)
        if translations:
            return translations[0].description
        return None
    display.short_description = lang_label
    return display


class ToiletIssueAdmin(OrderedModelAdmin):
    inlines = (
        ToiletIssueTranslationInline,
    )
    list_select_related = True
    list_display = (
        'value', 'move_up_down_links',
    ) + tuple(
        display_translation(lang, label)
        for lang, label in ToiletIssueTranslation.LANGUAGE_CHOICES
    )
    search_fields = (
        'value',
        'translations__description',
    )


admin.site.register(ToiletIssue, ToiletIssueAdmin)
