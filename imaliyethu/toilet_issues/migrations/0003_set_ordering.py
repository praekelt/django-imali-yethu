# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

import itertools

class Migration(DataMigration):

    def forwards(self, orm):
        # order issues by their primary key
        order = itertools.count()
        for issue in orm.ToiletIssue.objects.all().order_by('id'):
            issue.order = order.next()
            issue.save()

    def backwards(self, orm):
        # when going backwards, just leave ordering as is.
        pass

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
    symmetrical = True
