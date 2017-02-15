from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Host
from sshkm.forms import HostForm

from sshkm.views.deploy import *

from sshkm.tasks import *
from celery.task.control import inspect
from celery.result import AsyncResult
from celery import uuid
import celery


@login_required
def HostList(request):
    hosts = Host.objects.order_by('name')

    class HostStatus():
        def __init__(self, id, name, status):
            self.id = id
            self.name = name
            self.status = status

    hostsstati = []
    for host in hosts:
        try:
            status = celery.result.AsyncResult(host.task_id).status
        except:
            status = host.status
        hostsstati.append(HostStatus(host.id, host.name, status))

    context = {'hosts': hosts, 'hostsstati': hostsstati}
    return render(request, 'sshkm/host/list.html', context)

@login_required
def HostDetail(request):
    if request.method == 'GET' and 'id' in request.GET:
        host = get_object_or_404(Host, pk=request.GET['id'])
        hostform = HostForm(instance=host)
    else:
        hostform = HostForm()

    return render(request, 'sshkm/host/detail.html', {
        'hostform': hostform,
    })

@login_required
def HostDelete(request):
    try:
        if request.POST.get('id_multiple') is not None:
            Host.objects.filter(id__in=request.POST.getlist('id_multiple')).delete()
            messages.add_message(request, messages.SUCCESS, "Hosts deleted")
        else:
            host = Host.objects.get(id=request.GET['id'])
            delete = Host(id=request.GET['id']).delete()
            messages.add_message(request, messages.SUCCESS, "Host " + host.name + " deleted")
    except ObjectDoesNotExist as e:
        messages.add_message(request, messages.ERROR, "The host could not be deleted")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The host could not be deleted")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('HostList'))

@login_required
def HostSave(request):
    try:
        if request.POST.get('id') is not None:
            hostInstance = Host.objects.get(id=request.POST.get('id'))
            host = HostForm(request.POST, instance=hostInstance)
        else:
            host = HostForm(request.POST)
        host.save()
        messages.add_message(request, messages.SUCCESS, "Host " + request.POST.get('name') + " sucessfully saved")
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, "The host could not be saved.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The host could not be saved")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('HostList'))

@login_required
def HostDeploy(request):
    try:
        if request.POST.get('id_multiple') is not None:
            for host in request.POST.getlist('id_multiple'):
                task_id = uuid()
                deploy = ScheduleDeployKeys.apply_async([host], task_id=task_id)
                host = Host.objects.get(id=host)
                host.task_id = task_id
                host.save()
            messages.add_message(request, messages.INFO, "Multiple host deployment initiated")
        else:
            host = Host.objects.get(id=request.GET['id'])
            host.task_id = None
            try:
                DeployKeys(GetHostKeys(request.GET['id']), request.GET['id'])
                host.status = 'SUCCESS'
                messages.add_message(request, messages.SUCCESS, "Host " + host.name + " deployed")
            except:
                host = Host.objects.get(id=request.GET['id'])
                host.task_id = None
                host.status = 'FAILURE'
                messages.add_message(request, messages.ERROR, "Host " + host.name + " could not be deployed")
            host.save()
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The host could not be deployed")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('HostList'))
