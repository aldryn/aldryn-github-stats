# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import StringIO

from datetime import datetime, timedelta

from django.conf import settings
from django.core.cache import cache as memcache
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

from .utils import get_cache_key

from github import Github

CACHE_DURATION = getattr(settings, "ALDRYN_GITHUB_STATS_CACHE_DURATION", 3600)


@python_2_unicode_compatible
class GitHubStatsRepository(models.Model):

    label = models.CharField(
        max_length=128, default='', blank=False,
        help_text=_('Provide a descriptive label for your repo. E.g., '
                    '"django CMS'))
    full_name = models.CharField(
        max_length=255, blank=False, default='',
        help_text=_('Enter the repo. full name. E.g., "divio/django-cms"'),)
    token = models.CharField(
        max_length=64, blank=False, default='',
        help_text=_('Provide a suitable GitHub API token.'))

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _('repositories')
        unique_together = ('label', 'full_name', 'token')

    def __str__(self):
        return self.label

    def get_cache_key(self):
        """
        Gets the cache key for this specific repo configuration.
        """
        return get_cache_key(
            self.__class__.__name__, settings=(self.pk, ))

    def get_repo(self, force_refresh=False):
        """
        Using the configuration for this GitHubStatsRepository instance, fetch
        the repo object from cache, if possible, else, from GitHub.

        :param force_refresh: Set to force an update from GitHub.
        :type force_refresh: bool
        :rtype: GitHubStatsRepository
        """
        key = self.get_cache_key()
        g = Github(self.token)
        if force_refresh:
            repo = None
        else:
            pickled = memcache.get(key, None)
            if pickled:
                file_str = StringIO.StringIO(pickled)
                repo = g.load(file_str)
            else:
                repo = None
        if repo is None:
            repo = g.get_repo(self.full_name)
            output = StringIO.StringIO()
            g.dump(repo, output)
            duration = CACHE_DURATION * 2 if force_refresh else CACHE_DURATION
            memcache.set(key, output.getvalue(), duration)
        return repo


class GitHubStatsBase(CMSPlugin):
    # Avoid reverse relation name clashes by not adding a related_name
    # to the parent plugin
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True)
    repo = models.ForeignKey(
        'GitHubStatsRepository', null=True, verbose_name=_('repository'),
        help_text=_('Select the repository to work with.'))
    subhead = models.CharField(
        _('subhead'), max_length=255, blank=True, default='',
        help_text=_('Optional subheading.'))
    subhead_link = models.URLField(
        _('URL'), max_length=4096, blank=True, default='',
        help_text=_('Optional subhead link destination.'))

    class Meta:
        abstract = True


@python_2_unicode_compatible
class GitHubStatsRecentCommitsPluginModel(GitHubStatsBase):

    from_days_ago = models.PositiveIntegerField(
        _('Number of days ago'), default=30,
        validators=[MaxValueValidator(365), ],
        help_text=_('Number of days to sum commits (maximum 365)'))

    def recent_commits(self):
        if not self.repo or not self.repo.full_name or not self.repo.token:
            return 0
        key = get_cache_key(
            self.__class__.__name__,
            settings=(self.repo.full_name, self.repo.token, self.from_days_ago))

        cached_value = memcache.get(key)
        if cached_value is None:
            repo = self.repo.get_repo()
            if repo:
                today = datetime.today()
                days_ago = today - timedelta(days=self.from_days_ago or 0)
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
                if total is not None:
                    memcache.set(key, total, CACHE_DURATION)
            else:
                return 0
        return cached_value

    def __str__(self):
        return 'Recent commits for %d days on %s' % (
            self.from_days_ago,
            self.repo.full_name if self.repo else '',
        )


@python_2_unicode_compatible
class GitHubStatsIssuesCountPluginModel(GitHubStatsBase):

    CHOICES = (
        ('open', _('Open'), ),
        ('closed', _('Closed'), ),
    )

    from_days_ago = models.PositiveIntegerField(
        _('Number of days ago'), default=30,
        validators=[MaxValueValidator(365), ],
        help_text=_('Number of days to sum commits (maximum 365)'))
    state = models.CharField(
        max_length=16, choices=CHOICES, blank=False, default=CHOICES[1][0],
        help_text=_('Event type'))

    def recent_issues(self):
        if not self.repo or not self.repo.full_name or not self.repo.token:
            return 0
        key = get_cache_key(
            self.__class__.__name__,
            settings=(self.repo.full_name, self.repo.token, self.from_days_ago,
                      self.state))
        cached_value = memcache.get(key)
        if cached_value is None:
            repo = self.repo.get_repo()
            if repo:
                today = datetime.today()
                days_ago = today - timedelta(days=self.from_days_ago)

                issues = repo.get_issues(
                    state=self.state, since=days_ago)
                cached_value = len(list(issues))
                if cached_value is not None:
                    memcache.set(key, cached_value, CACHE_DURATION)
            else:
                return 0
        return cached_value

    def __str__(self):
        return 'Recent %s issues for %d days on %s' % (
            self.state.lower(),
            self.from_days_ago,
            self.repo.full_name if self.repo else ''
        )


@python_2_unicode_compatible
class GitHubStatsRepoPropertyPluginModel(GitHubStatsBase):

    CHOICES = (
        ('forks_count', _('No. forks'), ),
        ('network_count', _('No. networks'), ),
        ('open_issues_count', _('No. open issues'), ),
        ('size', _('Size'), ),
        ('stargazers_count', _('No. stargazers'), ),
        ('watchers_count', _('No. watchers'), ),
    )

    property_name = models.CharField(_('property'), max_length=64,
        blank=False, default=CHOICES[0][0], choices=CHOICES,
        help_text=_('Choose a repository property to display.'))

    property_label = models.CharField(_('label'), max_length=128,
        blank=False, default='',
        help_text=_('Label to display.'))

    def property(self):
        if not self.repo or not self.repo.full_name or not self.repo.token:
            return 0
        key = get_cache_key(
            self.__class__.__name__,
            settings=(self.repo.full_name, self.repo.token, self.property_name))
        cached_value = memcache.get(key)
        if cached_value is None:
            repo = self.repo.get_repo()
            if repo:
                cached_value = getattr(repo, self.property_name)
                if cached_value is not None:
                    memcache.set(key, cached_value, CACHE_DURATION)
            else:
                return 0
        return cached_value

    def __str__(self):
        return 'Property %s of "%s"' % (
            self.property_name,
            self.repo.full_name if self.repo else 'unset repo',
        )
