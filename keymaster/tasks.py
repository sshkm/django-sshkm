from __future__ import absolute_import, unicode_literals
from celery import shared_task, task

from keymaster.views.deploy import *

import time

@shared_task
def add(x, y):
    time.sleep(5)
    return x + y

@shared_task
def ScheduleDeployKeys(id):
    deploy = DeployKeys(GetHostKeys(id), id)

@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@task
def bla1(x, y):
    return x + y


