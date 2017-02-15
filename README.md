# still in initial development phase

# django-sshkm
django-sshkm is a Django based ssh-key management tool.
It stores ssh-public-keys in a database and combine them in goups (Development, Operations, Externals, ...). You can assign this groups to Operating System users on target hosts and are able to deploy your configurations.

# Requirements
- Linux
- RabbitMQ
- Django compatible database like (SQLite, MySQL/MariaDB, PostgreSQL, ...)

# Setup
::
  pip install https://github.com/sshkm/django-sshkm/archive/master.zip
