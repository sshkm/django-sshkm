from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Permission
from sshkm.forms import PermissionForm


@login_required
def PermissionList(request):
    permissions = Permission.objects.order_by('host_id')
    context = {'permissions': permissions}
    return render(request, 'sshkm/permission/list.html', context)

@login_required
def PermissionCreate(request):
    permissionform = PermissionForm()

    return render(request, 'sshkm/permission/create.html', {
        'permissionform': permissionform,
    })

@login_required
def PermissionDelete(request):
    try:
        if request.POST.get('id_multiple') is not None:
            Permission.objects.filter(id__in=request.POST.getlist('id_multiple')).delete()
            messages.add_message(request, messages.SUCCESS, "Permissions deleted")
        else:
            permission = Permission.objects.get(id=request.GET['id'])
            delete = Permission(id=request.GET['id']).delete()
            messages.add_message(request, messages.SUCCESS, "Permission " + permission.host.name + " -> " + permission.group.name + " -> " + permission.osuser.name + " deleted")
    except ObjectDoesNotExist as e:
        messages.add_message(request, messages.ERROR, "The permission could not be deleted")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The permission could not be deleted")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('PermissionList'))

@login_required
def PermissionSave(request):
    try:
        for host_id in request.POST.getlist('host'):
            for group_id in request.POST.getlist('group'):
                for osuser_id in request.POST.getlist('osuser'):
                    permission = Permission(host_id=host_id, group_id=group_id, osuser_id=osuser_id)
                    permission.save()
        messages.add_message(request, messages.SUCCESS, "Permission(s) sucessfully saved")
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, "One or more Permisson(s) already exists.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The permission could not be saved")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('PermissionList'))
