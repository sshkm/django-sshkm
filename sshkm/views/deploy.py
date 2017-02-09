import sys
import paramiko, base64, os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
#import time

from django.conf import settings

from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from sshkm.models import Group, Host, Osuser, Key, KeyGroup, Permission
#from .forms import KeyForm, KeyModelForm
from sshkm.forms import KeyForm


#@login_required
#def HostDeploy(request):
#    host = Host.objects.get(id=request.GET['id'])
#
#    # enable logging
#    #paramiko.util.log_to_file('ssh.log')
#
#    #key = paramiko.RSAKey(data=base64.decodestring('AAA...'))
#    client = paramiko.SSHClient()
#    client.load_system_host_keys()
#    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    #client.get_host_keys().add('ssh.example.com', 'ssh-rsa', key)
#    client.connect(host.name, username='root', key_filename='/opt/projects/admintools/id_rsa', timeout=5)
#    stdin, stdout, stderr = client.exec_command('ls')
#    for line in stdout:
#        print('... ' + line.strip('\n'))
#
#    sftp = client.open_sftp()
#    sftp.put('/tmp/test.txt', '/tmp/sftp.txt')
#    sftp.close()
#
#    client.close()
#
#    messages.add_message(request, messages.SUCCESS, "Host " + host.name + " deployed")
#    return redirect('/sshkm/host/list')

def CopyKeyfile(host, keyfile, osuser, home):
    # check python version make it compatible:
    if sys.version_info[0] < 3:
        pkey = StringIO.StringIO(settings.KEYMASTER_PRIVATE_KEY)
    else:
        pkey = StringIO(settings.KEYMASTER_PRIVATE_KEY)
    private_key = paramiko.RSAKey.from_private_key(pkey)
    pkey.close()

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    time.sleep(30)

    try:
        client.connect(host, username='root', pkey=private_key, timeout=5)

        client.exec_command('mkdir -p ' + home + '/.ssh')
        client.exec_command('chown ' + osuser + ' ' + home + '/.ssh')
        stdin, stdout, stderr = client.exec_command('echo "' + keyfile + '" > ' + home + '/.ssh/authorized_keys')
        ##for line in stdout:
        ##    print(line.strip('\n'))
        #print('chown ' + osuser + ' ' + home + '/.ssh/authorized_keys')
        client.exec_command('chown ' + osuser + ' ' + home + '/.ssh/authorized_keys')
        client.exec_command('chmod 600 ' + home + '/.ssh/authorized_keys')
        #print(host + " " + keyfile + " " + osuser + " " + home)

        client.close()
        return('OK')
    except Exception as e:
        raise
        return('ERROR')

def GetHostKeys(host_id):
    keys = []

    permissions = Permission.objects.filter(host_id=host_id).order_by('osuser_id')
    for permission in permissions:

        keygroups = KeyGroup.objects.filter(group_id=permission.group_id).order_by('key_id')
        for keygroup in keygroups:

            key = Key.objects.get(id=keygroup.key_id)
            osuser = Osuser.objects.get(id=permission.osuser_id)

            if key.publickey is not None and key.publickey != "":
                keys.append((GetHome(osuser.id), key.name, key.keytype,  key.publickey, osuser.name))
                #keyfile.append(SshKey(GetHome(osuser.id), key.name, 'key-type',  key.publickey, osuser.name))

    keys = sorted(set(keys))
    return keys

def DeployKeys(keys, host_id):
    host = Host.objects.get(id=host_id)

    config_masterkey = settings.KEYMASTER_PUBLIC_KEY
    #tmp_file = '/tmp/sshkm_key'

    last_home = keys[0][0]
    last_osuser = keys[0][4]
    masterkey = ''
    keyfile = ''
    counter = 0

    for key in keys:
        home = key[0]
        name = key[1]
        keytype = key[2]
        publickey = key[3]
        osuser = key[4]

        counter = counter + 1

        if counter == 1 and osuser == 'root':
            masterkey = config_masterkey + '\n'

        if home != last_home:
            if osuser == 'root':
                masterkey = config_masterkey + '\n'
            #print('ssh root@' + host.name + ' echo "' + keyfile + '" > ' + last_home + '/.ssh/authorized_keys')
            CopyKeyfile(host.name, keyfile, last_osuser, last_home)
            keyfile = masterkey + keytype + ' ' + publickey + ' ' + name + '\n'
        else:
            keyfile += masterkey + keytype + ' ' + publickey + ' ' + name + '\n'
        last_home = home
        last_osuser = osuser
        masterkey = ''

    #print('ssh root@' + host.name + ' echo "' + keyfile + '" > ' + last_home + '/.ssh/authorized_keys')
    CopyKeyfile(host.name, keyfile, last_osuser, last_home)

def GetHome(osuser_id):
    osuser = Osuser.objects.get(id=osuser_id)

    if osuser.home is None or osuser.home == "":
        if osuser.name == 'root':
            home = '/root'
        else:
            home = '/home/' + osuser.name
    else:
        home = osuser.home

    return home

