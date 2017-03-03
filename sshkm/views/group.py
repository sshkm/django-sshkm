from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Group, Key, KeyGroup, Permission
from sshkm.forms import GroupForm


@login_required
def GroupList(request):
    groups = Group.objects.order_by('name')
    context = {'groups': groups}
    return render(request, 'sshkm/group/list.html', context)

@login_required
def GroupDetail(request):
    if request.method == 'GET' and 'id' in request.GET:
        group = get_object_or_404(Group, pk=request.GET['id'])
        groupform = GroupForm(instance=group)
        permissions = Permission.objects.filter(group_id=request.GET['id'])
        members = Key.objects.all()
        members_selected = KeyGroup.objects.all().filter(group_id=request.GET['id'])
        ids_selected = []
        for member_selected in members_selected:
            ids_selected.append(member_selected.key_id)
        members_not_selected = Key.objects.all().exclude(id__in=ids_selected)
        return render(request, 'sshkm/group/detail.html', {
            'groupform': groupform,
            'permissions': permissions,
            'members': members,
            'members_selected': members_selected,
            'members_not_selected': members_not_selected,
        })
    else:
        groupform = GroupForm()
        members_not_selected = Key.objects.all()
        return render(request, 'sshkm/group/detail.html', {
            'groupform': groupform,
            'members_not_selected': members_not_selected,
        })

@login_required
def GroupDelete(request):
    try:
        if request.POST.get('id_multiple') is not None:
            Group.objects.filter(id__in=request.POST.getlist('id_multiple')).delete()
            messages.add_message(request, messages.SUCCESS, "Groups deleted")
        else:
            group = Group.objects.get(id=request.GET['id'])
            delete = Group(id=request.GET['id']).delete()
            messages.add_message(request, messages.SUCCESS, "Group " + group.name + " deleted")
    except ObjectDoesNotExist as e:
        messages.add_message(request, messages.ERROR, "The group could not be deleted")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The group could not be deleted")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('GroupList'))

@login_required
def GroupSave(request):
    try:
        if request.POST.get('id') is not None:
            group = Group(
                id=request.POST.get('id'),
                name=request.POST.get('name'),
                description=request.POST.get('description', ''),
            )
            KeyGroup.objects.filter(group_id=request.POST.get('id')).delete()
            group.save()
            for key_id in request.POST.getlist('members'):
                keygroup = KeyGroup(key_id=key_id, group_id=group.id)
                keygroup.save()
        else:
            group = Group(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
            )
            group.save()
            for key_id in request.POST.getlist('members'):
                keygroup = KeyGroup(key_id=key_id, group_id=group.id)
                keygroup.save()
        messages.add_message(request, messages.SUCCESS, "Group " + request.POST.get('name') + " sucessfully saved")
    except AttributeError as e:
        print(e)
        messages.add_message(request, messages.WARNING, "Group " + request.POST.get('name') + " sucessfully saved with warnings")
    except ValueError as e:
        print(e)
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, "The group could not be saved. Group already exists.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The group could not be saved")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('GroupList'))
