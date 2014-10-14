""" Toilet code models. """

from difflib import SequenceMatcher
import heapq

from django.utils.translation import ugettext_lazy as _
from django.db import models


class ToiletCode(models.Model):
    """ A model representing a toilet code. """

    TOILET_TYPE_CHOICES = (
        ("FT", _("Flush toilet")),
        ("TA", _("Tap")),
        ("SP", _("Stand pipe")),
    )

    code = models.CharField(max_length=32, help_text=_("Toilet code"))

    lat = models.FloatField(help_text=_("Latitude of the toilet"))
    lon = models.FloatField(help_text=_("Longitude of the toilet"))

    section = models.CharField(
        max_length=32, blank=True,
        help_text=_("Community section"))

    section_number = models.CharField(
        max_length=32, blank=True,
        help_text=_("Number within section"))

    cluster = models.CharField(
        max_length=32, blank=True,
        help_text=_("Cluster within section"))

    toilet_type = models.CharField(
        choices=TOILET_TYPE_CHOICES,
        max_length=32, blank=True,
        help_text=_("Toilet type"))

    def __unicode__(self):
        return unicode(self.code)

    @classmethod
    def nearest(cls, query, threshold=0.6, max_results=5):
        """ Search all the query codes and return the best matches.

        Uses :class:`difflib.SequenceMatcher` and :mod:`heapq`.
        """
        query = query.upper()
        matchers = (
            (code, SequenceMatcher(a=query, b=code.code.upper()))
            for code in cls.objects.all())
        results = heapq.nlargest(max_results, (
            (seq.ratio(), code.code, code)
            for code, seq in matchers
            if seq.real_quick_ratio() >= threshold and seq.ratio() >= threshold
        ))
        return [(ratio, code) for ratio, _, code in results]
