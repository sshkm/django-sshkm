import os, sys, site

from setuptools import find_packages, setup
from setuptools.command.install import install

version = '0.1.4'

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# check if sshkm.conf exists in /etc/sshkm directory and prevent from overwriting
if os.path.isfile("/etc/sshkm/sshkm.conf"):
    data_files = []
else:
    data_files = [('/etc/sshkm', ['sshkm.conf']),]

# post installation tasks
class install_post(install):
    def run(self):
        #
        # customized tasks
        #

        # get fresh django secret key
        from django.utils.crypto import get_random_string
        SECRET_KEY = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')

        # replacements in settings.py
        settings = 'sshkm/settings.py'
        f = open(settings, 'r')
        filedata = f.read()
        f.close()
        settings_content = filedata
        settings_content = settings_content.replace("'SECRET_KEY_PLACEHOLDER'", "'"+SECRET_KEY+"'")
        settings_content = settings_content.replace("DEBUG = True", "DEBUG = False")
        settings_content = settings_content.replace("SSHKM_VERSION = 'master'", "SSHKM_VERSION = '"+version+"'")
        f = open(settings, 'w')
        f.write(settings_content)
        f.close()

        #
        # run default install
        #
        install.run(self)

setup(
    name='django-sshkm',
    keywords=['ssh', 'keymaster', 'sshkm', 'ssh-key', 'public key', 'key management'],
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='GNU General Public License v3 (GPLv3)',
    description='A Django based ssh-key management tool.',
    long_description=README,
    url='https://github.com/sshkm/django-sshkm',
    download_url='https://github.com/sshkm/django-sshkm/archive/' + version + '.zip',
    author='Peter Loeffler',
    author_email='sshkm@guruz.at',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Natural Language :: German',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: System :: Systems Administration',
    ],
    install_requires=[
        'setuptools',
        'django>=1.8',
        'django-auth-ldap',
        'mysqlclient',
        'psycopg2',
        'celery>=4.0.0',
        'django-bootstrap3',
        'paramiko',
        'simplejson',
        'enum34',
        #'enum34;python_version<"3.4"',
    ],
    data_files=data_files,
    cmdclass={'install': install_post},
)
