from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Osuser, Permission
from sshkm.forms import OsuserForm


@login_required
def OsuserList(request):
    osusers = Osuser.objects.order_by('name')
    context = {'osusers': osusers}
    return render(request, 'sshkm/osuser/list.html', context)

@login_required
def OsuserDetail(request):
    if request.method == 'GET' and 'id' in request.GET:
        osuser = get_object_or_404(Osuser, pk=request.GET['id'])
        osuserform = OsuserForm(instance=osuser)
        permissions = Permission.objects.filter(osuser_id=request.GET['id'])
        return render(request, 'sshkm/osuser/detail.html', {
            'osuserform': osuserform,
            'permissions': permissions,
        })
    else:
        osuserform = OsuserForm()
        return render(request, 'sshkm/osuser/detail.html', {
            'osuserform': osuserform,
        })

@login_required
def OsuserDelete(request):
    try:
        if request.POST.get('id_multiple') is not None:
            Osuser.objects.filter(id__in=request.POST.getlist('id_multiple')).delete()
            messages.add_message(request, messages.SUCCESS, "Osusers deleted")
        else:
            osuser = Osuser.objects.get(id=request.GET['id'])
            delete = Osuser(id=request.GET['id']).delete()
            messages.add_message(request, messages.SUCCESS, "Osuser " + osuser.name + " deleted")
    except ObjectDoesNotExist as e:
        messages.add_message(request, messages.ERROR, "The osuser could not be deleted")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The osuser could not be deleted")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('OsuserList'))

@login_required
def OsuserSave(request):
    try:
        if request.POST.get('id') is not None:
            osuserInstance = Osuser.objects.get(id=request.POST.get('id'))
            osuser = OsuserForm(request.POST, instance=osuserInstance)
        else:
            osuser = OsuserForm(request.POST)
        osuser.save()
        messages.add_message(request, messages.SUCCESS, "Osuser " + request.POST.get('name') + " sucessfully saved")
    except IntegrityError as e:
        messages.add_message(request, messages.ERROR, "The osuser could not be saved.")
    except Exception as e:
        messages.add_message(request, messages.ERROR, "The osuser could not be saved")
        print(type(e))
        print(e)

    return HttpResponseRedirect(reverse('OsuserList'))
