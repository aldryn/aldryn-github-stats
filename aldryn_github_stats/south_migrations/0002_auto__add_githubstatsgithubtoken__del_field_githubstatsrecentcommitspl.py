# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GitHubStatsGitHubToken'
        db.create_table(u'aldryn_github_stats_githubstatsgithubtoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128)),
            ('token', self.gf('django.db.models.fields.CharField')(default=u'', max_length=64)),
        ))
        db.send_create_signal(u'aldryn_github_stats', ['GitHubStatsGitHubToken'])

        # Deleting field 'GitHubStatsRecentCommitsPluginModel.github_api_token'
        db.delete_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'github_api_token')

        # Adding field 'GitHubStatsRecentCommitsPluginModel.token'
        db.add_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'token',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldryn_github_stats.GitHubStatsGitHubToken'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'GitHubStatsGitHubToken'
        db.delete_table(u'aldryn_github_stats_githubstatsgithubtoken')

        # Adding field 'GitHubStatsRecentCommitsPluginModel.github_api_token'
        db.add_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'github_api_token',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=64),
                      keep_default=False)

        # Deleting field 'GitHubStatsRecentCommitsPluginModel.token'
        db.delete_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'token_id')


    models = {
        u'aldryn_github_stats.githubstatsgithubtoken': {
            'Meta': {'object_name': 'GitHubStatsGitHubToken'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64'})
        },
        u'aldryn_github_stats.githubstatsrecentcommitspluginmodel': {
            'Meta': {'object_name': 'GitHubStatsRecentCommitsPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'from_days_ago': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'repository': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_github_stats.GitHubStatsGitHubToken']", 'null': 'True'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        }
    }

    complete_apps = ['aldryn_github_stats']