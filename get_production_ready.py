from django.utils.crypto import get_random_string

print('running get_production_ready...')

SECRET_KEY = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')

f = open('sshkm/settings.py', 'r')
filedata = f.read()
f.close()

newdata = filedata.replace("'SECRET_KEY_PLACEHOLDER'", "'"+SECRET_KEY+"'")
newdata = newdata.replace("DEBUG = True", "DEBUG = False")

f = open('sshkm/settings.py', 'w')
f.write(newdata)
f.close()
