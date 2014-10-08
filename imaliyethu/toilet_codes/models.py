""" Toilet code models. """

from difflib import SequenceMatcher
import heapq

from django.utils.translation import ugettext_lazy as _
from django.db import models


class ToiletCode(models.Model):
    """ A model representing a toilet code. """

    code = models.CharField(max_length=32, help_text=_("Toilet code"))

    lat = models.FloatField(help_text=_("Latitude of the toilet"))
    lon = models.FloatField(help_text=_("Longitude of the toilet"))

    def __unicode__(self):
        return unicode(self.code)

    @classmethod
    def nearest(cls, query, threshold=0.6, max_results=5):
        """ Search all the query codes and return the best matches.

        Uses :class:`difflib.SequenceMatcher` and :mod:`heapq`.
        """
        results = []
        for code in cls.objects.all():
            s = SequenceMatcher(a=query, b=code.code)
            if s.real_quick_ratio() < threshold:
                continue
            item = (s.ratio(), code)
            if len(results) < max_results:
                heapq.heappush(results, item)
            else:
                heapq.heappushpop(results, item)
        return results
