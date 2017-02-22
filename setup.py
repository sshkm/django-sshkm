import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# check if sshkm.conf exists in /etc/sshkm directory and prevent from overwriting
if os.path.isfile("/etc/sshkm/sshkm.conf"):
    data_files = []
else:
    data_files = [('/etc/sshkm', ['sshkm.conf']),]

version = '0.1.2'

setup(
    name='django-sshkm',
    keywords=['ssh', 'keymaster', 'sshkm', 'ssh-key'],
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='GNU General Public License v3 (GPLv3)',
    description='A Django based ssh-key management tool.',
    long_description=README,
    url='https://github.com/sshkm/django-sshkm',
    download_url='https://github.com/sshkm/django-sshkm/archive/' + version + '.zip',
    author='Peter Loeffler',
    author_email='peter.loeffler@guruz.at',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
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
    #options = {'django-sshkm':{'post_install' : 'get_production_ready.py'}},
    options = {},
    post_script = 'get_production_ready.py',
)
