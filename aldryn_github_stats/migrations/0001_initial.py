# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubStatsIssuesCountPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('subhead', models.CharField(default='', help_text='Optional subheading.', max_length=255, verbose_name='subhead', blank=True)),
                ('subhead_link', models.URLField(default='', help_text='Optional subhead link destination.', max_length=4096, verbose_name='URL', blank=True)),
                ('from_days_ago', models.PositiveIntegerField(default=30, help_text='Number of days to sum commits (maximum 365)', verbose_name='Number of days ago', validators=[django.core.validators.MaxValueValidator(365)])),
                ('state', models.CharField(default='closed', help_text='Event type', max_length=16, choices=[('open', 'Open'), ('closed', 'Closed')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GitHubStatsRecentCommitsPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('subhead', models.CharField(default='', help_text='Optional subheading.', max_length=255, verbose_name='subhead', blank=True)),
                ('subhead_link', models.URLField(default='', help_text='Optional subhead link destination.', max_length=4096, verbose_name='URL', blank=True)),
                ('from_days_ago', models.PositiveIntegerField(default=30, help_text='Number of days to sum commits (maximum 365)', verbose_name='Number of days ago', validators=[django.core.validators.MaxValueValidator(365)])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GitHubStatsRepoPropertyPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('subhead', models.CharField(default='', help_text='Optional subheading.', max_length=255, verbose_name='subhead', blank=True)),
                ('subhead_link', models.URLField(default='', help_text='Optional subhead link destination.', max_length=4096, verbose_name='URL', blank=True)),
                ('property_name', models.CharField(default='forks_count', help_text='Choose a repository property to display.', max_length=64, verbose_name='property', choices=[('forks_count', 'No. forks'), ('network_count', 'No. networks'), ('open_issues_count', 'No. open issues'), ('size', 'Size'), ('stargazers_count', 'No. stargazers'), ('watchers_count', 'No. watchers')])),
                ('property_label', models.CharField(default='', help_text='Label to display.', max_length=128, verbose_name='label')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GitHubStatsRepository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(default='', help_text='Provide a descriptive label for your repo. E.g., "django CMS', max_length=128)),
                ('full_name', models.CharField(default='', help_text='Enter the repo. full name. E.g., "divio/django-cms"', max_length=255)),
                ('token', models.CharField(default='', help_text='Provide a suitable GitHub API token.', max_length=64)),
            ],
            options={
                'verbose_name': 'repository',
                'verbose_name_plural': 'repositories',
            },
        ),
        migrations.AlterUniqueTogether(
            name='githubstatsrepository',
            unique_together=set([('label', 'full_name', 'token')]),
        ),
        migrations.AddField(
            model_name='githubstatsrepopropertypluginmodel',
            name='repo',
            field=models.ForeignKey(verbose_name='repository', to='aldryn_github_stats.GitHubStatsRepository', help_text='Select the repository to work with.', null=True),
        ),
        migrations.AddField(
            model_name='githubstatsrecentcommitspluginmodel',
            name='repo',
            field=models.ForeignKey(verbose_name='repository', to='aldryn_github_stats.GitHubStatsRepository', help_text='Select the repository to work with.', null=True),
        ),
        migrations.AddField(
            model_name='githubstatsissuescountpluginmodel',
            name='repo',
            field=models.ForeignKey(verbose_name='repository', to='aldryn_github_stats.GitHubStatsRepository', help_text='Select the repository to work with.', null=True),
        ),
    ]
