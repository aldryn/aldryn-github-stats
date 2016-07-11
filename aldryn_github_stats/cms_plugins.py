# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from distutils.version import LooseVersion
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms import __version__ as cms_version
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models

CACHE_DURATION = getattr(settings, "ALDRYN_GITHUB_STATS_CACHE_DURATION", 3600)
CMS_GTE_330 = LooseVersion(cms_version) >= LooseVersion('3.3.0')


class GitHubStatsBasePlugin(CMSPluginBase):
    if not CMS_GTE_330:
        cache = False

    def get_cache_expiration(self, request, instance, placeholder):
        return CACHE_DURATION


class GitHubStatsRecentCommitsPlugin(GitHubStatsBasePlugin):
    module = 'GitHub Stats'
    render_template = 'aldryn_github_stats/plugins/recent_commits.html'
    name = _('Recent Commit Count')
    model = models.GitHubStatsRecentCommitsPluginModel

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(GitHubStatsRecentCommitsPlugin)


class GitHubStatsIssuesCountPlugin(GitHubStatsBasePlugin):
    module = 'GitHub Stats'
    render_template = 'aldryn_github_stats/plugins/recent_issues.html'
    name = _('Recent Issues Count')
    model = models.GitHubStatsIssuesCountPluginModel

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(GitHubStatsIssuesCountPlugin)


class GitHubStatsRepoPropertyPlugin(GitHubStatsBasePlugin):
    module = 'GitHub Stats'
    render_template = 'aldryn_github_stats/plugins/repo_property.html'
    name = _('Repo Property')
    model = models.GitHubStatsRepoPropertyPluginModel

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(GitHubStatsRepoPropertyPlugin)
