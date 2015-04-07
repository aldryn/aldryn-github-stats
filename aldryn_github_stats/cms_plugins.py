# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models


class GitHubStatsRecentCommitsPlugin(CMSPluginBase):
    module = 'GitHub Stats'
    render_template = 'aldryn_github_stats/plugins/recent_commits.html'
    name = _('Recent Commit Count')
    cache = False
    model = models.GitHubStatsRecentCommitsPluginModel

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(GitHubStatsRecentCommitsPlugin)


class GitHubStatsIssuesCountPlugin(CMSPluginBase):
    module = 'GitHub Stats'
    render_template = 'aldryn_github_stats/plugins/recent_issues.html'
    name = _('Recent Issues Count')
    cache = False
    model = models.GitHubStatsIssuesCountPluginModel

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(GitHubStatsIssuesCountPlugin)


class GitHubStatsRepoPropertyPlugin(CMSPluginBase):
    module = 'GitHub Stats'
    render_template = 'aldryn_github_stats/plugins/repo_property.html'
    name = _('Repo Property')
    cache = False
    model = models.GitHubStatsRepoPropertyPluginModel

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(GitHubStatsRepoPropertyPlugin)
