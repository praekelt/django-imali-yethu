""" Tools for mapping toilet codes to and from CSV. """

import csv
import math
import re

from imaliyethu.toilet_codes.models import ToiletCode


class ParseGPS(object):
    PATTERN = re.compile(r"""
        ^\s*^(?P<direction>[NEWS]?)
        \s*(?P<int>\d+)[.,](?P<frac>\d+)$
    """, re.VERBOSE)

    def __init__(self, pos_dir, neg_dir, decimal_point="."):
        self._pos_dir = pos_dir
        self._neg_dir = neg_dir
        self._decimal_point = decimal_point

    def parse(self, value):
        match = self.PATTERN.match(value)
        if match is None:
            return 0.0
        groups = match.groupdict()
        sign = -1.0 if (groups["direction"] == self._neg_dir) else 1.0
        return sign * float(groups["int"] + "." + groups["frac"])

    def format(self, value):
        direction = self._pos_dir if (value >= 0) else self._neg_dir
        gps = "%s%g" % (direction, math.fabs(value))
        return gps.replace(".", self._decimal_point)


class ToiletCodeCsv(object):

    model = ToiletCode

    update_field = "code"

    # CSV header -> model field
    fields = (
        ("Code", "code"),
        ("Section", "section"),
        ("Cluster", "cluster"),
        ("Number", "section_number"),
        ("Type", "toilet_type"),
        ("GPS Latitude", "lat"),
        ("GPS Longitude", "lon"),
    )

    field_formatters = {
        "lat": ParseGPS("N", "S"),
        "lon": ParseGPS("E", "W"),
    }

    def __init__(self):
        self._csv_fields = [csv for csv, _model in self.fields]
        self._to_csv_header = dict(
            (model, csv) for csv, model in self.fields)
        self._model_fields = [model for _csv, model in self.fields]
        self._from_csv_header = dict(
            (self.canonicalize_fieldname(csv), model)
            for csv, model in self.fields)

    def read_csv(self, file_obj):
        reader = csv.DictReader(file_obj)
        self.canonicalize_fieldnames(reader)
        for data in reader:
            model = self.data_to_model(data)
            if self.update_model(model):
                continue
            self.create_model(model)

    def write_csv(self, file_obj):
        writer = csv.DictWriter(file_obj, self._csv_fields)
        writer.writeheader()
        for obj in self.model.objects.all():
            writer.writerow(self.model_to_data(obj))

    def _format_obj_field(self, obj, field):
        value = getattr(obj, field)
        formatter = self.field_formatters.get(field)
        if formatter is not None:
            value = formatter.format(value)
        return value

    def model_to_data(self, obj):
        return dict(
            (self._to_csv_header.get(field, field),
             self._format_obj_field(obj, field))
            for field in self._model_fields
        )

    def canonicalize_fieldname(self, fieldname):
        return fieldname.strip().lower()

    def canonicalize_fieldnames(self, reader):
        fieldnames = [
            self.canonicalize_fieldname(f) for f in reader.fieldnames]
        # documented way to set fieldnames DictReader
        reader._fieldnames = fieldnames

    def data_to_model(self, data):
        kw = dict(
            (self._from_csv_header.get(field, field), data[field])
            for field in self._from_csv_header.iterkeys()
        )
        obj = self.model(**kw)
        for field, formatter in self.field_formatters.iteritems():
            setattr(obj, field, formatter.parse(getattr(obj, field)))
        return obj

    def create_model(self, obj):
        obj.save()

    def update_model(self, obj):
        kw = {}
        kw[self.update_field] = getattr(obj, self.update_field)
        try:
            existing = ToiletCode.objects.get(**kw)
        except ToiletCode.DoesNotExist:
            return False
        except ToiletCode.MultipleObjectsReturned:
            return False
        obj.pk = existing.pk
        obj.save()
        return True
