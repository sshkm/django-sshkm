from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Key, KeyGroup, Group
from sshkm.forms import KeyForm


@login_required
def KeyList(request):
    keys = Key.objects.order_by('name')
    context = {'keys': keys}
    return render(request, 'sshkm/key/list.html', context)

#import simplejson as json
#def task_state(request):
#    data = 'Fail'
#    if request.is_ajax():
#        if request.GET['task_id']:
#            task_id = request.GET['task_id']
#            task = AsyncResult(task_id)
#            data = task.result or task.state
#        else:
#            data = 'No task_id in the request'
#    else:
#        data = 'This is not an ajax request'
#
#    json_data = json.dumps(data)
#    return HttpResponse(json_data, content_type='application/json')

@login_required
def KeyDetail(request):
    if request.method == 'GET' and 'id' in request.GET:
        key = get_object_or_404(Key, pk=request.GET['id'])
        keyform = KeyForm(instance=key)
        groups = Group.objects.all()
        groups_selected = KeyGroup.objects.all().filter(key_id=request.GET['id'])
        ids_selected = []
        for group_selected in groups_selected:
            ids_selected.append(group_selected.group_id)
        groups_not_selected = Group.objects.all().exclude(id__in=ids_selected)
        return render(request, 'sshkm/key/detail.html', {
            'keyform': keyform,
            'groups': groups,
            'groups_selected': groups_selected,
            'groups_not_selected': groups_not_selected,
        })
    else:
        keyform = KeyForm()
        groups_not_selected = Group.objects.all()
        return render(request, 'sshkm/key/detail.html', {
            'keyform': keyform,
            'groups_not_selected': groups_not_selected,
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
                publickey=request.POST.get('publickey', False).replace("\n", "").replace("\r", ""),
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
                publickey=request.POST.get('publickey', False).replace("\n", "").replace("\r", ""),
            )
            key.save()
            for group_id in request.POST.getlist('member_of'):
                keygroup = KeyGroup(key_id=key.id, group_id=group_id)
                keygroup.save()
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
