# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Unit'
        db.create_table(u'xfit_unit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('plural', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['Unit'])

        # Adding model 'Gym'
        db.create_table(u'xfit_gym', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['Gym'])

        # Adding model 'Workout'
        db.create_table(u'xfit_workout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('is_hero', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('workout_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('time_limit', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['Workout'])

        # Adding model 'Exercise'
        db.create_table(u'xfit_exercise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['Exercise'])

        # Adding model 'WorkoutExercise'
        db.create_table(u'xfit_workoutexercise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workout', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exercises', to=orm['xfit.Workout'])),
            ('item_group', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('item_group_repeats', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('effort', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100)),
            ('effort_unit', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='+', null=True, blank=True, to=orm['xfit.Unit'])),
            ('exercise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xfit.Exercise'])),
            ('reps', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('reps_unit', self.gf('django.db.models.fields.related.ForeignKey')(default=2, related_name='+', null=True, blank=True, to=orm['xfit.Unit'])),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['WorkoutExercise'])

        # Adding model 'WorkoutOfTheDay'
        db.create_table(u'xfit_workoutoftheday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gym', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wods', to=orm['xfit.Gym'])),
            ('workout', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wods', to=orm['xfit.Workout'])),
            ('day', self.gf('django.db.models.fields.DateField')()),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['WorkoutOfTheDay'])

        # Adding unique constraint on 'WorkoutOfTheDay', fields ['gym', 'workout']
        db.create_unique(u'xfit_workoutoftheday', ['gym_id', 'workout_id'])

        # Adding model 'UserWOD'
        db.create_table(u'xfit_userwod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('wod', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xfit.WorkoutOfTheDay'])),
            ('time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('rounds', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['UserWOD'])

        # Adding model 'WODExercise'
        db.create_table(u'xfit_wodexercise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['xfit.WorkoutExercise'], null=True, blank=True)),
            ('user_wod', self.gf('django.db.models.fields.related.ForeignKey')(related_name='wod_exercises', to=orm['xfit.UserWOD'])),
            ('effort', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('reps', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'xfit', ['WODExercise'])


    def backwards(self, orm):
        # Removing unique constraint on 'WorkoutOfTheDay', fields ['gym', 'workout']
        db.delete_unique(u'xfit_workoutoftheday', ['gym_id', 'workout_id'])

        # Deleting model 'Unit'
        db.delete_table(u'xfit_unit')

        # Deleting model 'Gym'
        db.delete_table(u'xfit_gym')

        # Deleting model 'Workout'
        db.delete_table(u'xfit_workout')

        # Deleting model 'Exercise'
        db.delete_table(u'xfit_exercise')

        # Deleting model 'WorkoutExercise'
        db.delete_table(u'xfit_workoutexercise')

        # Deleting model 'WorkoutOfTheDay'
        db.delete_table(u'xfit_workoutoftheday')

        # Deleting model 'UserWOD'
        db.delete_table(u'xfit_userwod')

        # Deleting model 'WODExercise'
        db.delete_table(u'xfit_wodexercise')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'xfit.exercise': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Exercise'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'xfit.gym': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Gym'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'xfit.unit': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Unit'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'plural': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'xfit.userwod': {
            'Meta': {'ordering': "('-wod__day', 'user')", 'object_name': 'UserWOD'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rounds': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'wod': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xfit.WorkoutOfTheDay']"})
        },
        u'xfit.wodexercise': {
            'Meta': {'object_name': 'WODExercise'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'effort': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xfit.WorkoutExercise']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'reps': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_wod': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wod_exercises'", 'to': u"orm['xfit.UserWOD']"})
        },
        u'xfit.workout': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Workout'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_hero': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'time_limit': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'workout_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'})
        },
        u'xfit.workoutexercise': {
            'Meta': {'ordering': "('workout', 'item_group', 'order')", 'object_name': 'WorkoutExercise'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'effort': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'effort_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': u"orm['xfit.Unit']"}),
            'exercise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['xfit.Exercise']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_group': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'item_group_repeats': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'reps': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'reps_unit': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'related_name': "'+'", 'null': 'True', 'blank': 'True', 'to': u"orm['xfit.Unit']"}),
            'workout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exercises'", 'to': u"orm['xfit.Workout']"})
        },
        u'xfit.workoutoftheday': {
            'Meta': {'ordering': "('-day', 'gym__order')", 'unique_together': "(('gym', 'workout'),)", 'object_name': 'WorkoutOfTheDay'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'day': ('django.db.models.fields.DateField', [], {}),
            'gym': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wods'", 'to': u"orm['xfit.Gym']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'workout': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'wods'", 'to': u"orm['xfit.Workout']"})
        }
    }

    complete_apps = ['xfit']