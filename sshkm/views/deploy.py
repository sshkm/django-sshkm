import sys
import paramiko, base64, os

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

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

from sshkm.models import Group, Host, Osuser, Key, KeyGroup, Permission, Setting
from sshkm.forms import KeyForm


def CopyKeyfile(host, keyfile, osuser, home):
    try:
        key = Setting.objects.get(name='MasterKeyPrivate')
    except:
        messages.add_message(request, messages.ERROR, "Failed to get private key. Maybe not uploaded in Settings?")

    try:
        passphrase = Setting.objects.get(name='MasterKeyPrivatePassphrase').value
    except:
        passphrase = None

    pkey = StringIO(key.value)
    if passphrase:
        private_key = paramiko.RSAKey.from_private_key(pkey, password=passphrase)
    else:
        private_key = paramiko.RSAKey.from_private_key(pkey)
    pkey.close()

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username='root', pkey=private_key, timeout=5)

        client.exec_command('mkdir -p ' + home + '/.ssh')
        client.exec_command('chown ' + osuser + ' ' + home + '/.ssh')
        stdin, stdout, stderr = client.exec_command('echo "' + keyfile + '" > ' + home + '/.ssh/authorized_keys')
        client.exec_command('chown ' + osuser + ' ' + home + '/.ssh/authorized_keys')
        client.exec_command('chmod 600 ' + home + '/.ssh/authorized_keys')

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
                keys.append((GetHome(osuser.id), key.publickey, osuser.name))

    keys = sorted(set(keys))
    return keys

def DeployKeys(keys, host_id):
    try:
        key = Setting.objects.get(name='MasterKeyPublic')
    except:
        messages.add_message(request, messages.ERROR, "Failed to get public key. Maybe not uploaded in Settings?")

    host = Host.objects.get(id=host_id)

    config_masterkey = key.value

    last_home = keys[0][0]
    last_osuser = keys[0][2]
    masterkey = ''
    keyfile = ''
    counter = 0

    for key in keys:
        home = key[0]
        publickey = key[1]
        osuser = key[2]

        counter = counter + 1

        if counter == 1 and osuser == 'root':
            masterkey = config_masterkey + '\n'

        if home != last_home:
            if osuser == 'root':
                masterkey = config_masterkey + '\n'
            CopyKeyfile(host.name, keyfile, last_osuser, last_home)
            keyfile = masterkey + publickey + '\n'
        else:
            keyfile += masterkey + publickey + '\n'
        last_home = home
        last_osuser = osuser
        masterkey = ''

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

