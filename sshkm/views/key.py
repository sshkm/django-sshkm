from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Key, Group, KeyGroup
from sshkm.forms import KeyForm

from sshkm.views.deploy import *


@login_required
def KeyList(request):
    keys = Key.objects.order_by('name')
    context = {'keys': keys}

#    i = 0
#    tasks = []
#    while i < 5:
#        tasks.append(uuid())
#        i = i + 1
#
#    i = 0
#    for task in tasks:
#        #print(task)
#        res = add.apply_async((2, i), task_id=task)
#        i = i + 1
#
#    ins = inspect()
#    for a in ins.registered_tasks():
#        print(a)
#
#    from celery import current_app
#    #current_app.loader.import_default_modules()
#    all_task_names = current_app.tasks.keys()
#    all_tasks = current_app.tasks.values()
#    foo_task = current_app.tasks['sshkm.tasks.add']
#    print(type(foo_task))
#
#    for a in all_tasks:
#        print(a.subtask)
#
#    #all_task_classes = [type(task) for task in current_app.tasks.itervalues()]
#
#    #from itertools import chain
#    #print(set(chain.from_iterable( ins.registered_tasks().values() )))
#
#    #task_id = uuid()
#    #print(task_id)
#    #res = add.apply_async((2, 2), task_id=task_id)
#
#    result = celery.result.AsyncResult('45d7985a-9ccb-4f67-8aad-e29e1e42ea86')
#    print(result.status)
#    print(result.result)
#
#    print(dir(celery.result.current_app.tasks.items))
#    print(celery.result.current_app.tasks.values)
#
#    #for a in celery.result.current_app.tasks.keys:
#    #    print(a)

    return render(request, 'sshkm/key/list.html', context)

import simplejson as json
def task_state(request):
    data = 'Fail'
    if request.is_ajax():
        #if 'task_id' in request.POST.keys() and request.POST['task_id']:
        if request.GET['task_id']:
            task_id = request.GET['task_id']
            task = AsyncResult(task_id)
            data = task.result or task.state
        else:
            data = 'No task_id in the request'
    else:
        data = 'This is not an ajax request'

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')

@login_required
def KeyDetail(request):
    if request.method == 'GET' and 'id' in request.GET:
        key = get_object_or_404(Key, pk=request.GET['id'])
        #for bla in key.is_in.all():
        #    print(bla.name)
        keyform = KeyForm(instance=key)
    else:
        keyform = KeyForm()

    return render(request, 'sshkm/key/detail.html', {
        'keyform': keyform,
    })

@login_required
def KeyDelete(request):
    try:
        if request.POST.get('id_multiple') is not None:
            Key.objects.filter(id__in=request.POST.getlist('id_multiple')).delete()
            messages.add_message(request, messages.SUCCESS, "Keys deleted")
        else:
            key = Key.objects.get(id=request.GET['id'])
            delete = Key(id=request.GET['id']).delete()
            messages.add_message(request, messages.SUCCESS, "Key " + key.name + " deleted")
    except ObjectDoesNotExist as e:
        messages.add_message(request, messages.ERROR, "The key could not be deleted. Key does not exist")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The key could not be deleted")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('KeyList'))

@login_required
def KeySave(request):
    try:
        if request.POST.get('id') is not None:
            key = Key(
                id=request.POST.get('id'),
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
                firstname=request.POST.get('firstname', False),
                lastname=request.POST.get('lastname', False),
                email=request.POST.get('email'),
                keytype=request.POST.get('keytype', False),
                publickey=request.POST.get('publickey', False),
            )
            KeyGroup.objects.filter(key_id=request.POST.get('id')).delete()
            key.save()
            for group_id in request.POST.getlist('member_of'):
                keygroup = KeyGroup(key_id=key.id, group_id=group_id)
                keygroup.save()
        else:
            key = Key(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                firstname=request.POST.get('firstname', False),
                lastname=request.POST.get('lastname', False),
                email=request.POST.get('email'),
                keytype=request.POST.get('keytype', False),
                publickey=request.POST.get('publickey', False),
            )
            key.save()
            for group_id in request.POST.getlist('member_of'):
                keygroup = KeyGroup(key_id=key.id, group_id=group_id)
                keygroup.save()
        #key.save()
        messages.add_message(request, messages.SUCCESS, "Key " + request.POST.get('name') + " sucessfully saved")
    except AttributeError as e:
        print(e)
        messages.add_message(request, messages.WARNING, "Key " + request.POST.get('name') + " sucessfully saved with warnings")
    except ValueError as e:
        print(e)
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, "The key could not be saved. Key already exists.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The key could not be saved")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('KeyList'))
