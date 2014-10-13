# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ToiletCode.section'
        db.add_column(u'toilet_codes_toiletcode', 'section',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'ToiletCode.section_number'
        db.add_column(u'toilet_codes_toiletcode', 'section_number',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'ToiletCode.cluster'
        db.add_column(u'toilet_codes_toiletcode', 'cluster',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)

        # Adding field 'ToiletCode.toilet_type'
        db.add_column(u'toilet_codes_toiletcode', 'toilet_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ToiletCode.section'
        db.delete_column(u'toilet_codes_toiletcode', 'section')

        # Deleting field 'ToiletCode.section_number'
        db.delete_column(u'toilet_codes_toiletcode', 'section_number')

        # Deleting field 'ToiletCode.cluster'
        db.delete_column(u'toilet_codes_toiletcode', 'cluster')

        # Deleting field 'ToiletCode.toilet_type'
        db.delete_column(u'toilet_codes_toiletcode', 'toilet_type')


    models = {
        u'toilet_codes.toiletcode': {
            'Meta': {'object_name': 'ToiletCode'},
            'cluster': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'section': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'section_number': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'toilet_type': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['toilet_codes']