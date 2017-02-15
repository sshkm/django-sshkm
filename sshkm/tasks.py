from __future__ import absolute_import, unicode_literals
from celery import shared_task

from sshkm.views.deploy import DeployKeys, GetHostKeys

# task to deploy ssh-keys to hosts
@shared_task
def ScheduleDeployKeys(id):
    deploy = DeployKeys(GetHostKeys(id), id)

