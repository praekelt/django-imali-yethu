""" Toilet issue models. """

from django.utils.translation import ugettext_lazy as _
from django.db import models


class ToiletIssue(models.Model):
    """ A model representing a common problem with a toilet. """
    value = models.CharField(
        max_length=1024,
        help_text=_("Value to store in the report."))

    def __unicode__(self):
        return unicode(self.value)


class ToiletIssueTranslation(models.Model):
    """ A translation of a description of a problem with a toilet. """

    LANGUAGE_CHOICES = (
        ("en", "English"),
        ("xh", "Xhosa"),
    )

    issue = models.ForeignKey(
        ToiletIssue,
        related_name="translations",
        help_text=_("Issue that this translation is for."))
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        max_length=128,
        help_text=_("Language this translation is in."))
    description = models.CharField(
        max_length=1024,
        help_text=_("A description of the issue in this language."))

    def __unicode__(self):
        return u"%s (%s, %s)" % (
            self.description, self.language, self.issue.value)
