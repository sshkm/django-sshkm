Name:		sshkm
Version:	0.1.2
Release:	1%{?dist}
Summary:	SSHKM

Group:		Applications/Internet
License:	GNU General Public License v3 (GPLv3)
URL:		https://github.com/sshkm/django-sshkm
Source0:	%{name}-%{version}-%{release}.tar.bz2

BuildRequires:	gcc, python, python-virtualenv, python-devel, python-pip, mariadb-devel, postgresql-devel, openldap-devel, httpd-devel, sqlite, rabbitmq-server, httpd, mod_wsgi
Requires:	python, python-virtualenv, sqlite, rabbitmq-server, httpd, mod_wsgi

%description
A Django based ssh-key management tool

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
cp -av opt $RPM_BUILD_ROOT
cp -av etc $RPM_BUILD_ROOT

virtualenv /opt/sshkm
source /opt/sshkm/bin/activate
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/appdirs-1.4.0-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/six-1.10.0-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/pyparsing-2.1.10-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/pycparser-2.17.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/packaging-16.8-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/cffi-1.9.1-cp27-cp27mu-manylinux1_x86_64.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/idna-2.2-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/setuptools-34.2.0-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/enum34-1.1.6-py2-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/vine-1.1.3-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/amqp-2.1.4-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/billiard-3.5.0.2.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/pyasn1-0.2.2-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/ipaddress-1.0.18-py2-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/cryptography-1.7.2.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/kombu-4.0.2-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/mysqlclient-1.3.10.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/paramiko-2.1.2-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/psycopg2-2.6.2.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/python-ldap-2.4.32.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/pytz-2016.10-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/simplejson-3.10.0.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/celery-4.0.2-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/Django-1.10.5-py2.py3-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/django_auth_ldap-1.2.9-py2-none-any.whl
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/django-bootstrap3-8.1.0.tar.gz
pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/django-sshkm-0.1.2.tar.gz
#pip install /root/rpmbuild/BUILD/sshkm-0.1.2/sources/mod_wsgi-4.5.14.tar.gz
#mod_wsgi-express install-module
deactivate

cat >/opt/sshkm/bin/celery << EOL
#!/opt/sshkm/bin/python
__requires__ = 'celery==4.0.2'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('celery==4.0.2', 'console_scripts', 'celery')()
    )
EOL
chmod 755 /opt/sshkm/bin/celery

mkdir -p $RPM_BUILD_ROOT/opt
cp -a /opt/sshkm $RPM_BUILD_ROOT/opt/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/sshkm
/etc/sshkm
/etc/httpd/conf.d/sshkm.conf
/etc/systemd/system/sshkm-celery.service
/etc/sysconfig/sshkm-celery
%doc

%post
id -g sshkm &>/dev/null || groupadd sshkm
id -u sshkm &>/dev/null || useradd -g sshkm -M -s /sbin/nologin sshkm
mkdir -p /var/run/sshkm/celery
mkdir -p /var/log/sshkm/celery
chown sshkm:sshkm /var/log/sshkm/celery /var/run/sshkm/celery

chown sshkm /etc/sshkm
chown sshkm:sshkm /etc/sshkm/db.sqlite3
chmod 770 /etc/sshkm/db.sqlite3

systemctl daemon-reload

systemctl enable rabbitmq-server.service
systemctl restart rabbitmq-server.service

systemctl enable sshkm-celery.service
systemctl restart sshkm-celery.service

systemctl enable httpd.service
systemctl restart httpd.service

%changelog
