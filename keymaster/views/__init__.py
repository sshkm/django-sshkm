import paramiko, base64, os

from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from keymaster.models import Group, Host, Osuser, Key, KeyGroup, Permission
#from .forms import KeyForm, KeyModelForm
from keymaster.forms import KeyForm



from keymaster.views.help import help
from keymaster.views.key import *
from keymaster.views.group import *
from keymaster.views.host import *
from keymaster.views.osuser import *
from keymaster.views.permission import *
from keymaster.views.deploy import *
from keymaster.views.settings import *



@login_required
def index(request):
    return render(request, 'keymaster/index.html')

#def GetKeys(keys, server_id):
#    server = Server.objects.get(id=server_id)
#
#    last_home = ''
#    masterkey = ''
#
#    for k in keys:
#        if k[0] != last_home or last_home == '':
#            redirector = '>'
#            if k[4] == 'root':
#                masterkey = 'masterkey\n'
#        else:
#            redirector = '>>'
#            masterkey = ''
#        print('ssh root@' + server.name + ' echo "' + masterkey + k[2] + ' ' + k[3] + ' ' + k[1] + '" ' + redirector + ' ' + k[0] + '/.ssh/authorized_keys')
#        last_home = k[0]


#def DeployKeys2(keyfile, server_id):
#    server = Server.objects.get(id=server_id)
#
#    last_home = keyfile[0].home
#    masterkey = ''
#    keyout = ''
#    counter = 0
#
#    for k in keyfile:
#        counter = counter + 1
#
#        if counter == 1 and k.sysuser == 'root':
#            masterkey = 'masterkey\n'
#
#        if k.home != last_home:
#            if k.sysuser == 'root':
#                masterkey = 'masterkey\n'
#            print('ssh root@' + server.name + ' echo "' + keyout + '" > ' + last_home + '/.ssh/authorized_keys')
#            keyout = masterkey + k.keytype + ' ' + k.key + ' ' + k.email + '\n'
#        else:
#            keyout += masterkey + k.keytype + ' ' + k.key + ' ' + k.email + '\n'
#        last_home = k.home
#        masterkey = ''
#
#    print('ssh root@' + server.name + ' echo "' + keyout + '" > ' + last_home + '/.ssh/authorized_keys')


