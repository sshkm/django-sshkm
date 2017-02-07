import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version = '0.1'

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
    #download_url='https://github.com/sshkm/django-sshkm/archive/' + version + '.zip',
    download_url='https://github.com/sshkm/django-sshkm/archive/master.zip',
    author='Peter Loeffler',
    author_email='peter.loeffler@guruz.at',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
    install_requires=[
        'setuptools',
        'django>=1.8',
        'django-auth-ldap',
        'celery>=4.0.0',
        'django-bootstrap3',
        'paramiko',
#        'simplejson',
    ],
)
