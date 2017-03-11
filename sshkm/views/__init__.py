from django.conf import settings as dsettings
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from sshkm.models import Setting

from sshkm.views.docs import docs
from sshkm.views.key import KeyList, KeyDetail, KeyDelete, KeySave
from sshkm.views.group import GroupList, GroupDetail, GroupDelete, GroupSave
from sshkm.views.host import HostList, HostDetail, HostDelete, HostSave, HostDeploy
from sshkm.views.osuser import OsuserList, OsuserDetail, OsuserDelete, OsuserSave
from sshkm.views.permission import PermissionList, PermissionCreate, PermissionDelete, PermissionSave
from sshkm.views.deploy import CopyKeyfile, GetHostKeys, DeployKeys, GetHome
from sshkm.views.settings import SettingsList, PasswordSave, CreateUser, DeleteUser, MasterKeyPublic, MasterKeyPrivate, Superuser


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
    if user is not None and user.is_active:
        login(request, user)
        return redirect('/')
    else:
        sshkm_version = dsettings.SSHKM_VERSION
        return render(request, 'sshkm/login.html', {'sshkm_version': sshkm_version})

@login_required
def auth_logout(request):
    logout(request)
    return redirect('/')

