# django-sshkm [![Build Status](https://travis-ci.org/sshkm/django-sshkm.svg?branch=master)](https://travis-ci.org/sshkm/django-sshkm)
### still under heavy construction!!!
django-sshkm is a Django based ssh-key management tool.  
It stores ssh-public-keys in a database and combine them in goups (Development, Operations, Externals, ...). You can assign these groups to Operating System users on target hosts and are able to deploy your configurations.  
  
Do you have hundreds of hosts/servers and dozens of users or other systems which want to connect to these using SSH?  
Do you know the problem when some employee leaves the company but knows many passwords of OS-users and now you should better change all your passwords?  
Do you want to have better control over who can connect to your hosts using SSH?  
Then django-sshkm is perfect for you.

## Requirements
- Linux
- RabbitMQ
- Python >= 2.7
- Django >= 1.8
- Celery >= 4.0.0
- Django compatible database like (SQLite, MySQL/MariaDB, PostgreSQL, ...)

## Setup
- Install a RabbitMQ server.
- Install a Django compatible database.
- Install SSHKM:  
  you will need some development tools and libraries: gcc python python-devel python-pip mariadb-devel postgresql-devel openldap-devel httpd-devel  
```bash
pip install django-sshkm
```
- Configure /etc/sshkm/sshkm.conf  
  If you use sqlite make shure that the user running celery has read and write permissions to the db-file.
- Install a webserver which runs wsgi  
  Example Apache httpd:  
```
Alias /static/ /usr/lib/python2.7/site-packages/sshkm/static/

<Directory /usr/lib/python2.7/site-packages/sshkm/static/>
  Require all granted
</Directory>

WSGIScriptAlias / /usr/lib/python2.7/site-packages/sshkm/wsgi.py
WSGIDaemonProcess sshkm user=apache group=apache
WSGIProcessGroup sshkm

<Directory /usr/lib/python2.7/site-packages>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>
```
- Run celery  
```
celery worker -A sshkm -l info
```

You can find a full example for a runnable versions in the wiki: https://github.com/sshkm/django-sshkm/wiki
