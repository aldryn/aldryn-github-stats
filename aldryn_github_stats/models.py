# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime, timedelta

from django.core.cache import cache as memcache
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from github import Github

ONE_HOUR = 3600


class GitHubStatsBase(CMSPlugin):
    # avoid reverse relation name clashes by not adding a related_name
    # to the parent plugin
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class GitHubStatsRecentCommitsPluginModel(GitHubStatsBase):

    repository = models.CharField(max_length=255, blank=False, default='',
        help_text=_('Enter the repo. full name. E.g., "divio/django-cms"'))

    from_days_ago = models.PositiveIntegerField(
        _('Number of days ago'),
        default=30,
        help_text=_('Number of days to sum commits (maximum 365)'),
        validators=[MaxValueValidator(365), ]
    )

    github_api_token = models.CharField(max_lenth=64, blank=False, default='',
        help_text=_('Provide a suitable GitHub API token.'))

    def recent_commits(self):
        cache_key = 'GitHubStatsPlugin:recent_commits:{0}'.format(
            self.from_days_ago)
        cached_value = memcache.get(cache_key)
        if not cached_value:
            g = Github(self.github_api_token)
            repo = g.get_repo(self.repository)
            if repo:
                today = datetime.today()
                days_ago = today - timedelta(days=self.from_days_ago)

                total = 0
                for commits in repo.get_stats_commit_activity():
                    delta = commits.week - days_ago
                    if delta.days > -7:
                        if delta.days < 0:
                            for num in commits.days[-delta.days:]:
                                total += num
                        else:
                            total += commits.total
                memcache.set(cache_key, total, ONE_HOUR)
            else:
                return 0
        return cached_value

    def __str__(self):
        return 'Recent commits for %d days' % self.from_days_ago
