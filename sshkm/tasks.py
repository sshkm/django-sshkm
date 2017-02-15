from __future__ import absolute_import, unicode_literals
from celery import shared_task, task

from sshkm.views.deploy import *

@shared_task
def ScheduleDeployKeys(id):
    deploy = DeployKeys(GetHostKeys(id), id)

