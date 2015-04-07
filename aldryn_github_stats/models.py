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


@python_2_unicode_compatible
class GitHubStatsGitHubToken(models.Model):

    label = models.CharField(max_length=128, default='', blank=False,
        help_text=_('Provide a descriptive label for your token.'))

    token = models.CharField(max_length=64, blank=False, default='',
        help_text=_('Provide a suitable GitHub API token.'))

    class Meta:
        verbose_name = _('GitHub API Token')
        verbose_name_plural = _('GitHub API Tokens')

    def __str__(self):
        return self.label


class GitHubStatsBase(CMSPlugin):
    # avoid reverse relation name clashes by not adding a related_name
    # to the parent plugin
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True)

    token = models.ForeignKey('GitHubStatsGitHubToken', null=True,
        help_text=_('Please select a token to use for this plugin.'))

    class Meta:
        abstract = True

    def get_cache_key(self, settings=()):
        """
        Returns the suitable key for *this* instance and settings.

        Provide a tuple hashable types that should be considered in the hash.
        Typically, this will be the settings that will be used in the calculated
        value that would be cached.

        E.g., key = self.get_cache_key(('divio/django-cms', 'abc123xyz...', 90))
        """
        cls_name = self.__class__.__name__
        return '{0}:{1}:{2}'.format(cls_name, self.pk, hash(tuple(settings)))


@python_2_unicode_compatible
class GitHubStatsRecentCommitsPluginModel(GitHubStatsBase):

    repository = models.CharField(max_length=255, blank=False, default='',
        help_text=_('Enter the repo. full name. E.g., "divio/django-cms"'))

    from_days_ago = models.PositiveIntegerField(_('Number of days ago'),
        default=30, validators=[MaxValueValidator(365), ],
        help_text=_('Number of days to sum commits (maximum 365)'))

    def recent_commits(self):
        if not self.token or not self.token.token:
            return 0
        key = self.get_cache_key([
            self.repository, self.token.token, self.from_days_ago])
        cached_value = memcache.get(key)
        if cached_value is None:
            g = Github(self.token.token)
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
                cached_value = total
                memcache.set(key, total, ONE_HOUR)
            else:
                return 0
        return cached_value

    def __str__(self):
        return 'Recent commits for %d days' % self.from_days_ago
