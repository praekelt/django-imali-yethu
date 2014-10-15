# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ToiletIssue.order'
        db.add_column(u'toilet_issues_toiletissue', 'order',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ToiletIssue.order'
        db.delete_column(u'toilet_issues_toiletissue', 'order')


    models = {
        u'toilet_issues.toiletissue': {
            'Meta': {'ordering': "('order',)", 'object_name': 'ToiletIssue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'toilet_issues.toiletissuetranslation': {
            'Meta': {'object_name': 'ToiletIssueTranslation'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['toilet_issues.ToiletIssue']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['toilet_issues']
