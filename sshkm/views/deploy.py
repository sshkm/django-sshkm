from django.utils import timezone
import paramiko

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from sshkm.models import Host, Osuser, Key, KeyGroup, Permission, Setting


def CopyKeyfile(host, keyfile, osuser, home, superuser):
    hostupdate = Host.objects.get(name=host)
    hostupdate.status = 'PENDING'
    hostupdate.last_status = timezone.now()
    hostupdate.save()

    key = Setting.objects.get(name='MasterKeyPrivate')

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
        client.connect(host, username=superuser, pkey=private_key, timeout=5)

        client.exec_command('mkdir -p ' + home + '/.ssh')
        client.exec_command('chown ' + osuser + ' ' + home + '/.ssh')
        stdin, stdout, stderr = client.exec_command('echo "' + keyfile + '" > ' + home + '/.ssh/authorized_keys')
        client.exec_command('chown ' + osuser + ' ' + home + '/.ssh/authorized_keys')
        client.exec_command('chmod 600 ' + home + '/.ssh/authorized_keys')

        client.close()

        hostupdate.status = 'SUCCESS'
        hostupdate.last_status = timezone.now()
        hostupdate.save()

        return('OK')
    except Exception as e:
        hostupdate.status = 'FAILURE'
        hostupdate.last_status = timezone.now()
        hostupdate.save()

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
    host = Host.objects.get(id=host_id)

    if len(keys) == 0:
        host.status = 'SUCCESS'
        host.last_status = timezone.now()
        host.save()
        # ToDo: return nothing to deploy
    else:
        key = Setting.objects.get(name='MasterKeyPublic')

        host.status = 'PENDING'
        host.last_status = timezone.now()
        host.save()

        try:
            globalsuperuser = Setting.objects.get(name='SuperUser').value
        except:
            globalsuperuser = False

        if host.superuser and host.superuser != "":
            superuser = host.superuser
        else:
            if globalsuperuser and globalsuperuser != "":
                superuser = globalsuperuser
            else:
                superuser = 'root'

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

            if counter == 1 and osuser == superuser:
                masterkey = config_masterkey + '\n'

            if home != last_home:
                if osuser == superuser:
                    masterkey = config_masterkey + '\n'
                CopyKeyfile(host.name, keyfile, last_osuser, last_home, superuser)
                keyfile = masterkey + publickey + '\n'
            else:
                keyfile += masterkey + publickey + '\n'
            last_home = home
            last_osuser = osuser
            masterkey = ''

        CopyKeyfile(host.name, keyfile, last_osuser, last_home, superuser)

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

