# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Paste.title'
        db.alter_column(u'paste_paste', 'title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Paste.title'
        raise RuntimeError("Cannot reverse this migration. 'Paste.title' and its values cannot be restored.")

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