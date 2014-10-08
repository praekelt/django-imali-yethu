# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ToiletIssue'
        db.create_table(u'toilet_issues_toiletissue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'toilet_issues', ['ToiletIssue'])

        # Adding model 'ToiletIssueTranslation'
        db.create_table(u'toilet_issues_toiletissuetranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['toilet_issues.ToiletIssue'])),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'toilet_issues', ['ToiletIssueTranslation'])


    def backwards(self, orm):
        # Deleting model 'ToiletIssue'
        db.delete_table(u'toilet_issues_toiletissue')

        # Deleting model 'ToiletIssueTranslation'
        db.delete_table(u'toilet_issues_toiletissuetranslation')


    models = {
        u'toilet_issues.toiletissue': {
            'Meta': {'object_name': 'ToiletIssue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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