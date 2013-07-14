# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Query'
        db.create_table(u'keywords_query', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'keywords', ['Query'])

        # Adding model 'Edge'
        db.create_table(u'keywords_edge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('head', self.gf('django.db.models.fields.related.ForeignKey')(related_name='outging_edge_set', to=orm['keywords.Query'])),
            ('tail', self.gf('django.db.models.fields.related.ForeignKey')(related_name='incoming_edge_set', to=orm['keywords.Query'])),
        ))
        db.send_create_signal(u'keywords', ['Edge'])


    def backwards(self, orm):
        # Deleting model 'Query'
        db.delete_table(u'keywords_query')

        # Deleting model 'Edge'
        db.delete_table(u'keywords_edge')


    models = {
        u'keywords.edge': {
            'Meta': {'object_name': 'Edge'},
            'head': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'outging_edge_set'", 'to': u"orm['keywords.Query']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tail': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'incoming_edge_set'", 'to': u"orm['keywords.Query']"})
        },
        u'keywords.query': {
            'Meta': {'object_name': 'Query'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['keywords']