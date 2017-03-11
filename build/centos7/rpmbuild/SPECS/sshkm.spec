Name:		sshkm
Version:	0.1.4
Release:	1%{?dist}
Summary:	SSHKM

Group:		Applications/System
License:	GNU General Public License v3 (GPLv3)
URL:		https://github.com/sshkm/django-sshkm
Source0:	%{name}-%{version}-%{release}.tar.bz2

BuildRequires:	gcc, python, python-virtualenv, python-devel, python-pip, mariadb-devel, postgresql-devel, openldap-devel, httpd-devel, sqlite, rabbitmq-server, httpd, mod_wsgi
Requires:	python, python-virtualenv, sqlite, rabbitmq-server, httpd, mod_wsgi
AutoReqProv:    no

%description
A Django based ssh-key management tool


%define sourcedir %{_builddir}/%{name}-%{version}


%prep
%setup -q

%install
export QA_RPATHS=$[ 0x0001|0x0002 ]
mkdir -p $RPM_BUILD_ROOT
cp -av opt $RPM_BUILD_ROOT
cp -av etc $RPM_BUILD_ROOT

virtualenv %{sourcedir}/opt/sshkm
source %{sourcedir}/opt/sshkm/bin/activate
#pip install %{sourcedir}/sources/pip-9.0.1-py2.py3-none-any.whl --upgrade
pip install %{sourcedir}/sources/appdirs-1.4.3-py2.py3-none-any.whl
pip install %{sourcedir}/sources/six-1.10.0-py2.py3-none-any.whl
pip install %{sourcedir}/sources/pyparsing-2.2.0-py2.py3-none-any.whl
pip install %{sourcedir}/sources/pycparser-2.17.tar.gz
pip install %{sourcedir}/sources/packaging-16.8-py2.py3-none-any.whl
pip install %{sourcedir}/sources/cffi-1.9.1-cp27-cp27mu-manylinux1_x86_64.whl
pip install %{sourcedir}/sources/idna-2.5-py2.py3-none-any.whl
pip install %{sourcedir}/sources/setuptools-34.3.1-py2.py3-none-any.whl
pip install %{sourcedir}/sources/enum34-1.1.6-py2-none-any.whl
pip install %{sourcedir}/sources/vine-1.1.3-py2.py3-none-any.whl
pip install %{sourcedir}/sources/amqp-2.1.4-py2.py3-none-any.whl
pip install %{sourcedir}/sources/billiard-3.5.0.2.tar.gz
pip install %{sourcedir}/sources/pyasn1-0.2.3-py2.py3-none-any.whl
pip install %{sourcedir}/sources/ipaddress-1.0.18-py2-none-any.whl
pip install %{sourcedir}/sources/cryptography-1.8.1.tar.gz
pip install %{sourcedir}/sources/asn1crypto-0.21.1-py2.py3-none-any.whl
pip install %{sourcedir}/sources/kombu-4.0.2-py2.py3-none-any.whl
pip install %{sourcedir}/sources/mysqlclient-1.3.10.tar.gz
pip install %{sourcedir}/sources/paramiko-2.1.2-py2.py3-none-any.whl
pip install %{sourcedir}/sources/psycopg2-2.7-cp27-cp27mu-manylinux1_x86_64.whl
pip install %{sourcedir}/sources/python-ldap-2.4.32.tar.gz
pip install %{sourcedir}/sources/pytz-2016.10-py2.py3-none-any.whl
pip install %{sourcedir}/sources/simplejson-3.10.0.tar.gz
pip install %{sourcedir}/sources/celery-4.0.2-py2.py3-none-any.whl
pip install %{sourcedir}/sources/Django-1.10.6-py2.py3-none-any.whl
pip install %{sourcedir}/sources/django_auth_ldap-1.2.10-py2-none-any.whl
pip install %{sourcedir}/sources/django-bootstrap3-8.2.1.tar.gz
pip install %{sourcedir}/sources/django-sshkm-0.1.4.tar.gz
deactivate
virtualenv --relocatable %{sourcedir}/opt/sshkm

cat >%{sourcedir}/opt/sshkm/bin/celery << EOL
#!/opt/sshkm/bin/python
__requires__ = 'celery==4.0.2'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('celery==4.0.2', 'console_scripts', 'celery')()
    )
EOL
chmod 755 %{sourcedir}/opt/sshkm/bin/celery

#echo "FIXING virtualenv PATHS"
#find -H %{sourcedir}/opt/sshkm -type f | while read filename;
#do
#     perl -p -i.bak -e "s|%{sourcedir}||g" ${filename}
#     if [ -f ${filename}.bak ]; then
#        rm -f ${filename}.bak
#        echo "FIXED ${filename}"
#     fi
#done

mkdir -p %{buildroot}/opt
cp -a %{sourcedir}/opt/sshkm %{buildroot}/opt/

%clean
%{__rm} -rf $RPM_BUILD_ROOT %{sourcedir}

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
