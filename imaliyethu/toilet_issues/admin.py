""" Toilet issue admin settings. """

from django.contrib import admin

from imaliyethu.toilet_issues.models import ToiletIssue, ToiletIssueTranslation


class ToiletIssueTranslationInline(admin.TabularInline):
    model = ToiletIssueTranslation
    extra = 1


def display_translation(lang_code, lang_label):
    """ Construct a function for displaying a column of translations. """
    def display(issue):
        for trans in issue.translations.all():
            if trans.language == lang_code:
                return trans.description
        return None
    display.short_description = lang_label
    return display


class ToiletIssueAdmin(admin.ModelAdmin):
    inlines = (
        ToiletIssueTranslationInline,
    )
    list_select_related = True
    list_display = (
        'value',
    ) + tuple(
        display_translation(lang, label)
        for lang, label in ToiletIssueTranslation.LANGUAGE_CHOICES
    )
    search_fields = (
        'value',
        'translations__description',
    )


admin.site.register(ToiletIssue, ToiletIssueAdmin)
