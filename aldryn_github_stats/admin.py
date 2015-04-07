# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from . import models


class GitHubStatsGitHubTokenAdminForm(forms.ModelForm):
    class Meta:
        model = models.GitHubStatsGitHubToken
        widgets = {
            'token' : forms.PasswordInput(),
        }


class GitHubStatsGitHubTokenAdmin(admin.ModelAdmin):
    form = GitHubStatsGitHubTokenAdminForm

admin.site.register(models.GitHubStatsGitHubToken, GitHubStatsGitHubTokenAdmin)