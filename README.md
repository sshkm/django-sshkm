# !!! still under heavy construction

# django-sshkm
django-sshkm is a Django based ssh-key management tool.
It stores ssh-public-keys in a database and combine them in goups (Development, Operations, Externals, ...). You can assign this groups to Operating System users on target hosts and are able to deploy your configurations.

## Requirements
- Linux
- RabbitMQ
- Django compatible database like (SQLite, MySQL/MariaDB, PostgreSQL, ...)

## Setup
```bash
pip install https://github.com/sshkm/django-sshkm/archive/master.zip
```
If you use sqlite make shure that the user running celery has read and write permissions to the db-file.

You can find a full example for a running version in the wiki: https://github.com/sshkm/django-sshkm/wiki/CentOS-7-example-setup-%28python-3.4-from-epel%29
