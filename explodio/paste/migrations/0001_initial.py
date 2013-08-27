# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Paste'
        db.create_table(u'paste_paste', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='python', max_length=100)),
            ('style', self.gf('django.db.models.fields.CharField')(default='monokai', max_length=100)),
            ('code', self.gf('django.db.models.fields.TextField')()),
            ('highlighted', self.gf('django.db.models.fields.TextField')()),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'paste', ['Paste'])


    def backwards(self, orm):
        # Deleting model 'Paste'
        db.delete_table(u'paste_paste')


    models = {
        u'paste.paste': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Paste'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {}),
            'highlighted': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'python'", 'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'monokai'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['paste']