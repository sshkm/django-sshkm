from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from keymaster.models import Host
from keymaster.forms import HostForm

from keymaster.views.deploy import *

from keymaster.tasks import *
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

#    #stati = [[]]
#    #stati = Stati()
#    #status = []
#    for host in hosts:
#        print(celery.result.AsyncResult(host.task_id).status)
#        #stati.append([host.id, celery.result.AsyncResult(host.task_id).status])
#        stati = Stati(host.id, celery.result.AsyncResult(host.task_id).status)
#        #status[host.id] = celery.result.AsyncResult(host.task_id).status

    hostsstati = []
    for host in hosts:
        try:
            status = celery.result.AsyncResult(host.task_id).status
        except:
            status = host.status
        hostsstati.append(HostStatus(host.id, host.name, status))

    #context = {'hosts': hosts}
    context = {'hosts': hosts, 'hostsstati': hostsstati}
    return render(request, 'keymaster/host/list.html', context)

@login_required
def HostDetail(request):
    if request.method == 'GET' and 'id' in request.GET:
        host = get_object_or_404(Host, pk=request.GET['id'])
        hostform = HostForm(instance=host)
    else:
        hostform = HostForm()

    return render(request, 'keymaster/host/detail.html', {
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
            #host = Host(
            #    id=request.POST.get('id'),
            #    name=request.POST.get('name'),
            #    description=request.POST.get('description', ''),
            #)
            hostInstance = Host.objects.get(id=request.POST.get('id'))
            host = HostForm(request.POST, instance=hostInstance)
            #host.is_valid()
            #host.cleaned_data
        else:
            #host = Host(
            #    name=request.POST.get('name'),
            #    description=request.POST.get('description'),
            #)
            host = HostForm(request.POST)
            #host.is_valid()
            #host.cleaned_data
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
                #print(host)
                task_id = uuid()
                deploy = ScheduleDeployKeys.apply_async([host], task_id=task_id)
                #DeployKeys(GetHostKeys(host), host)
                host = Host.objects.get(id=host)
                host.task_id = task_id
                host.save()
                #messages.add_message(request, messages.SUCCESS, "Hosts " + host + " deployed")
            messages.add_message(request, messages.INFO, "Multiple host deployment initiated")
        else:
            #task_id = uuid()
            #deploy = ScheduleDeployKeys.apply_async([request.GET['id']], task_id=task_id)
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
'''
    i = 0
    tasks = []
    while i < 5:
        tasks.append(uuid())
        i = i + 1

    i = 0
    for task in tasks:
        #print(task)
        res = add.apply_async((2, i), task_id=task)
        i = i + 1

    ins = inspect()
    for a in ins.registered_tasks():
        print(a)

    from celery import current_app
    #current_app.loader.import_default_modules()
    all_task_names = current_app.tasks.keys()
    all_tasks = current_app.tasks.values()
    foo_task = current_app.tasks['sshkm.tasks.add']
    print(type(foo_task))

    for a in all_tasks:
        print(a.subtask)

    #all_task_classes = [type(task) for task in current_app.tasks.itervalues()]

    #from itertools import chain
    #print(set(chain.from_iterable( ins.registered_tasks().values() )))

    #task_id = uuid()
    #print(task_id)
    #res = add.apply_async((2, 2), task_id=task_id)

    result = celery.result.AsyncResult('45d7985a-9ccb-4f67-8aad-e29e1e42ea86')
    print(result.status)
    print(result.result)

    print(dir(celery.result.current_app.tasks.items))
    print(celery.result.current_app.tasks.values)

    #for a in celery.result.current_app.tasks.keys:
    #    print(a)
'''



@login_required
def HostDeployOld(request):
    try:
        if request.POST.get('id_multiple') is not None:
            for host in request.POST.getlist('id_multiple'):
                #print(host)
                DeployKeys(GetHostKeys(host), host)
                messages.add_message(request, messages.SUCCESS, "Hosts " + host + " deployed")
        else:
            DeployKeys(GetHostKeys(request.GET['id']), request.GET['id'])
            #DeployKeys(GetHostKeys(request.GET['id']), request.GET['id'])
            host = Host.objects.get(id=request.GET['id'])
            #delete = Host(id=request.GET['id']).delete()
            messages.add_message(request, messages.SUCCESS, "Host " + host.name + " deployed")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The host could not be deployed")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('HostList'))
