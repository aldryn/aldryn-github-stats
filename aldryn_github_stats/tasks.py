# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from celery.schedules import schedule
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from django.conf import settings

from .models import GitHubStatsRepository

logger = get_task_logger(__name__)

CACHE_DURATION = getattr(settings, "ALDRYN_GITHUB_STATS_CACHE_DURATION", 3600)


@periodic_task(run_every=(schedule(run_every=CACHE_DURATION)))
def update_github_objects():
    """
    Asynchronously puts populated GitHub statistical objects into the cache.
    """
    # For every defined repo, get the repo object
    for config in GitHubStatsRepository.objects.all():
        repo = config.get_repo(force_refresh=True)
        logger.info(
            'GitHubStatsRepository ID:{0} repo loaded.'.format(config.pk))
