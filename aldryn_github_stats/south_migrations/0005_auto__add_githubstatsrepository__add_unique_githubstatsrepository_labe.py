# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GitHubStatsRepository'
        db.create_table(u'aldryn_github_stats_githubstatsrepository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128)),
            ('repository', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255)),
            ('token', self.gf('django.db.models.fields.CharField')(default=u'', max_length=64)),
        ))
        db.send_create_signal(u'aldryn_github_stats', ['GitHubStatsRepository'])

        # Adding unique constraint on 'GitHubStatsRepository', fields ['label', 'repository', 'token']
        db.create_unique(u'aldryn_github_stats_githubstatsrepository', ['label', 'repository', 'token'])

        # Adding field 'GitHubStatsIssuesCountPluginModel.repo'
        db.add_column(u'aldryn_github_stats_githubstatsissuescountpluginmodel', 'repo',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['aldryn_github_stats.GitHubStatsRepository'], null=True),
                      keep_default=False)

        # Adding field 'GitHubStatsRecentCommitsPluginModel.repo'
        db.add_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'repo',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['aldryn_github_stats.GitHubStatsRepository'], null=True),
                      keep_default=False)

        # Adding field 'GitHubStatsRepoPropertyPluginModel.repo'
        db.add_column(u'aldryn_github_stats_githubstatsrepopropertypluginmodel', 'repo',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['aldryn_github_stats.GitHubStatsRepository'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'GitHubStatsRepository', fields ['label', 'repository', 'token']
        db.delete_unique(u'aldryn_github_stats_githubstatsrepository', ['label', 'repository', 'token'])

        # Deleting model 'GitHubStatsRepository'
        db.delete_table(u'aldryn_github_stats_githubstatsrepository')

        # Deleting field 'GitHubStatsIssuesCountPluginModel.repo'
        db.delete_column(u'aldryn_github_stats_githubstatsissuescountpluginmodel', 'repo_id')

        # Deleting field 'GitHubStatsRecentCommitsPluginModel.repo'
        db.delete_column(u'aldryn_github_stats_githubstatsrecentcommitspluginmodel', 'repo_id')

        # Deleting field 'GitHubStatsRepoPropertyPluginModel.repo'
        db.delete_column(u'aldryn_github_stats_githubstatsrepopropertypluginmodel', 'repo_id')


    models = {
        u'aldryn_github_stats.githubstatsgithubtoken': {
            'Meta': {'object_name': 'GitHubStatsGitHubToken'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64'})
        },
        u'aldryn_github_stats.githubstatsissuescountpluginmodel': {
            'Meta': {'object_name': 'GitHubStatsIssuesCountPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'from_days_ago': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['aldryn_github_stats.GitHubStatsRepository']", 'null': 'True'}),
            'repository': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "u'closed'", 'max_length': '16'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'subhead_link': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '4096', 'blank': 'True'}),
            'token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_github_stats.GitHubStatsGitHubToken']", 'null': 'True'})
        },
        u'aldryn_github_stats.githubstatsrecentcommitspluginmodel': {
            'Meta': {'object_name': 'GitHubStatsRecentCommitsPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'from_days_ago': ('django.db.models.fields.PositiveIntegerField', [], {'default': '30'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['aldryn_github_stats.GitHubStatsRepository']", 'null': 'True'}),
            'repository': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'subhead_link': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '4096', 'blank': 'True'}),
            'token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_github_stats.GitHubStatsGitHubToken']", 'null': 'True'})
        },
        u'aldryn_github_stats.githubstatsrepopropertypluginmodel': {
            'Meta': {'object_name': 'GitHubStatsRepoPropertyPluginModel'},
            'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'+'", 'unique': 'True', 'primary_key': 'True', 'to': "orm['cms.CMSPlugin']"}),
            'property_label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128'}),
            'property_name': ('django.db.models.fields.CharField', [], {'default': "u'forks_count'", 'max_length': '64'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['aldryn_github_stats.GitHubStatsRepository']", 'null': 'True'}),
            'repository': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
            'subhead': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'subhead_link': ('django.db.models.fields.URLField', [], {'default': "u''", 'max_length': '4096', 'blank': 'True'}),
            'token': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aldryn_github_stats.GitHubStatsGitHubToken']", 'null': 'True'})
        },
        u'aldryn_github_stats.githubstatsrepository': {
            'Meta': {'unique_together': "((u'label', u'repository', u'token'),)", 'object_name': 'GitHubStatsRepository'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128'}),
            'repository': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255'}),
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