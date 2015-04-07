# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'GitHubStatsRepository', fields ['label', 'repository', 'token']
        db.delete_unique(u'aldryn_github_stats_githubstatsrepository', ['label', 'repository', 'token'])

        # Deleting model 'GitHubStatsGitHubToken'
        db.delete_table(u'aldryn_github_stats_githubstatsgithubtoken')

        # Deleting field 'GitHubStatsIssuesCountPluginModel.repository'
        db.delete_column(u'aldryn_github_stats_githubstatsissuescountpluginmodel', 'repository')

        # Deleting field 'GitHubStatsIssuesCountPluginModel.token'
        db.delete_column(u'aldryn_github_stats_githubstatsissuescountpluginmodel', 'token_id')

        # Deleting field 'GitHubStatsRecentCommitsPluginModel.token'
        db.delete_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'token_id')

        # Deleting field 'GitHubStatsRecentCommitsPluginModel.repository'
        db.delete_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'repository')

        # Deleting field 'GitHubStatsRepository.repository'
        db.delete_column(u'aldryn_github_stats_githubstatsrepository', 'repository')

        # Adding field 'GitHubStatsRepository.full_name'
        db.add_column(u'aldryn_github_stats_githubstatsrepository', 'full_name',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)

        # Adding unique constraint on 'GitHubStatsRepository', fields ['label', 'full_name', 'token']
        db.create_unique(u'aldryn_github_stats_githubstatsrepository', ['label', 'full_name', 'token'])

        # Deleting field 'GitHubStatsRepoPropertyPluginModel.token'
        db.delete_column(u'aldryn_github_stats_githubstatsrepopropertypluginmodel', 'token_id')

        # Deleting field 'GitHubStatsRepoPropertyPluginModel.repository'
        db.delete_column(u'aldryn_github_stats_githubstatsrepopropertypluginmodel', 'repository')


    def backwards(self, orm):
        # Removing unique constraint on 'GitHubStatsRepository', fields ['label', 'full_name', 'token']
        db.delete_unique(u'aldryn_github_stats_githubstatsrepository', ['label', 'full_name', 'token'])

        # Adding model 'GitHubStatsGitHubToken'
        db.create_table(u'aldryn_github_stats_githubstatsgithubtoken', (
            ('token', self.gf('django.db.models.fields.CharField')(default=u'', max_length=64)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128)),
        ))
        db.send_create_signal(u'aldryn_github_stats', ['GitHubStatsGitHubToken'])

        # Adding field 'GitHubStatsIssuesCountPluginModel.repository'
        db.add_column(u'aldryn_github_stats_githubstatsissuescountpluginmodel', 'repository',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)

        # Adding field 'GitHubStatsIssuesCountPluginModel.token'
        db.add_column(u'aldryn_github_stats_githubstatsissuescountpluginmodel', 'token',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldryn_github_stats.GitHubStatsGitHubToken'], null=True),
                      keep_default=False)

        # Adding field 'GitHubStatsRecentCommitsPluginModel.token'
        db.add_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'token',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldryn_github_stats.GitHubStatsGitHubToken'], null=True),
                      keep_default=False)

        # Adding field 'GitHubStatsRecentCommitsPluginModel.repository'
        db.add_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'repository',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)

        # Adding field 'GitHubStatsRepository.repository'
        db.add_column(u'aldryn_github_stats_githubstatsrepository', 'repository',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)

        # Deleting field 'GitHubStatsRepository.full_name'
        db.delete_column(u'aldryn_github_stats_githubstatsrepository', 'full_name')

        # Adding unique constraint on 'GitHubStatsRepository', fields ['label', 'repository', 'token']
        db.create_unique(u'aldryn_github_stats_githubstatsrepository', ['label', 'repository', 'token'])

        # Adding field 'GitHubStatsRepoPropertyPluginModel.token'
        db.add_column(u'aldryn_github_stats_githubstatsrepopropertypluginmodel', 'token',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aldryn_github_stats.GitHubStatsGitHubToken'], null=True),
                      keep_default=False)

        # Adding field 'GitHubStatsRepoPropertyPluginModel.repository'
        db.add_column(u'aldryn_github_stats_githubstatsrepopropertypluginmodel', 'repository',
                      self.gf('django.db.models.fields.CharField')(default=u'', max_length=255),
                      keep_default=False)


    models = {
        u'aldryn_github_stats.githubstatsissuescountpluginmodel': {
            'Meta': {'object_name': 'GitHubStatsIssuesCountPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'from_days_ago': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_github_stats.GitHubStatsRepository']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'closed'", 'max_length': '16'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'subhead_link': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '4096', 'blank': 'True'})
        },
        u'aldryn_github_stats.githubstatsrecentcommitspluginmodel': {
            'Meta': {'object_name': 'GitHubStatsRecentCommitsPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'from_days_ago': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_github_stats.GitHubStatsRepository']", 'null': 'True'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'subhead_link': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '4096', 'blank': 'True'})
        },
        u'aldryn_github_stats.githubstatsrepopropertypluginmodel': {
            'Meta': {'object_name': 'GitHubStatsRepoPropertyPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'property_label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128'}),
            'property_name': ('django.db.models.fields.CharField', [], {'default': "u'forks_count'", 'max_length': '64'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_github_stats.GitHubStatsRepository']", 'null': 'True'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'subhead_link': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '4096', 'blank': 'True'})
        },
        u'aldryn_github_stats.githubstatsrepository': {
            'Meta': {'unique_together': "((u'label', u'full_name', u'token'),)", 'object_name': 'GitHubStatsRepository'},
            'full_name': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64'})
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