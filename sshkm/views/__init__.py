#import paramiko, base64, os

#from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect, render
#from django.http import HttpResponseRedirect, HttpResponse
#from django.core.urlresolvers import reverse
#from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

#from django.db import IntegrityError
#from django.core.exceptions import ObjectDoesNotExist

#from sshkm.models import Group, Host, Osuser, Key, KeyGroup, Permission
#from .forms import KeyForm, KeyModelForm
#from sshkm.forms import KeyForm



from sshkm.views.docs import *
from sshkm.views.key import *
from sshkm.views.group import *
from sshkm.views.host import *
from sshkm.views.osuser import *
from sshkm.views.permission import *
from sshkm.views.deploy import *
from sshkm.views.settings import *



@login_required
def index(request):
    # show first steps if public/private keys are not uploaded
    keys = Setting.objects.filter(name__in=['MasterKeyPrivate', 'MasterKeyPublic']).count()
    if keys != 2:
        return render(request, 'sshkm/firststeps.html')
    else:
        return render(request, 'sshkm/docs.html')

def auth_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    if username is None:
        username = ''

    if password is None:
        password = ''

    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'sshkm/login.html')

@login_required
def auth_logout(request):
    logout(request)
    return redirect('/')

