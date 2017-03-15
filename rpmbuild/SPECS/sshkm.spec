Name:		sshkm
Version:	0.1.8
Release:	1%{?dist}
Summary:	A Python/Django based ssh-key management tool
Group:		Applications/System
License:	GNU General Public License v3 (GPLv3)
URL:		https://github.com/sshkm/django-sshkm
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	gcc, python, python-virtualenv, python-devel, python-pip, mariadb-devel, postgresql-devel, openldap-devel, httpd-devel, sqlite, rabbitmq-server, httpd, mod_wsgi
Requires:	python, python-virtualenv, sqlite, rabbitmq-server, httpd, mod_wsgi, policycoreutils-python
AutoReqProv:    no

%description
A Python/Django based ssh-key management tool
For more information visit https://github.com/sshkm/django-sshkm


%define sourcedir %{_builddir}/%{name}-%{version}
%define swdir /usr/lib


%prep
%setup -q


%install
export QA_RPATHS=$[ 0x0001|0x0002 ]
mkdir -p $RPM_BUILD_ROOT/%{swdir}
cp -av etc $RPM_BUILD_ROOT

virtualenv %{sourcedir}/%{swdir}/%{name}
source %{sourcedir}/%{swdir}/%{name}/bin/activate
%{sourcedir}/%{swdir}/%{name}/bin/pip install pip --upgrade
deactivate
source %{sourcedir}/%{swdir}/%{name}/bin/activate
if [ "%{version}" == "master" ]; then
    %{sourcedir}/%{swdir}/%{name}/bin/pip install https://github.com/sshkm/django-sshkm/archive/%{version}.tar.gz
else
    %{sourcedir}/%{swdir}/%{name}/bin/pip install django-sshkm==%{version}
fi
%define celery_version $(%{sourcedir}/%{swdir}/%{name}/bin/pip list --format=columns | grep celery | awk '{print $2}')
deactivate
virtualenv --relocatable %{sourcedir}/%{swdir}/%{name}

cat >%{sourcedir}/%{swdir}/%{name}/bin/celery << EOL
#!/%{swdir}/%{name}/bin/python
__requires__ = 'celery==%{celery_version}'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('celery==%{celery_version}', 'console_scripts', 'celery')()
    )
EOL
chmod 755 %{sourcedir}/%{swdir}/%{name}/bin/celery

mkdir -p %{buildroot}/%{swdir}
cp -a %{sourcedir}/%{swdir}/%{name} %{buildroot}/%{swdir}/


%clean
%{__rm} -rf $RPM_BUILD_ROOT %{sourcedir}


%files
%defattr(-,root,root,-)
/%{swdir}/%{name}
/etc/%{name}
/etc/httpd/conf.d/%{name}.conf
/etc/systemd/system/%{name}-celery.service
/etc/sysconfig/%{name}-celery
%doc


%post
PYTHONLIB=%{swdir}/%{name}/lib
PYTHONDIR=$PYTHONLIB/$(ls $PYTHONLIB)

# create user and group
id -g %{name} &>/dev/null || groupadd %{name}
id -u %{name} &>/dev/null || useradd -g %{name} -M -s /sbin/nologin %{name}

# create directories for pid file and logs
mkdir -p /var/run/%{name}/celery
mkdir -p /var/log/%{name}/celery
chown %{name}:%{name} /var/log/%{name}/celery /var/run/%{name}/celery

# grant permission for httpd
chown -R %{name} $PYTHONDIR/site-packages/%{name}

# SELinux
semanage fcontext -a -t httpd_sys_rw_content_t "$PYTHONDIR/site-packages/%{name}/db.sqlite3" 2> /dev/null
restorecon -v "$PYTHONDIR/site-packages/%{name}/db.sqlite3" 2> /dev/null
semanage fcontext -a -t httpd_sys_rw_content_t "$PYTHONDIR/site-packages/%{name}" 2> /dev/null
restorecon -v "$PYTHONDIR/site-packages/%{name}" 2> /dev/null
setsebool -P httpd_can_network_connect 1 2> /dev/null

# generate random SECRET_KEY
SECRET_KEY=$(python -c "from django.utils.crypto import get_random_string; print(get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789\!@#$%^&*(-_=+)'));")
sed -i "s/SECRET_KEY = .*/SECRET_KEY = '$SECRET_KEY'/g" $PYTHONDIR/site-packages/sshkm/settings.py

# enable and start all deamons
systemctl daemon-reload
systemctl enable rabbitmq-server.service
systemctl restart rabbitmq-server.service
systemctl enable %{name}-celery.service
systemctl restart %{name}-celery.service
systemctl enable httpd.service
systemctl restart httpd.service


%preun
systemctl stop %{name}-celery.service


%postun
# on removal
if [ "$1" == "0" ]; then
    # SELinux
    setsebool -P httpd_can_network_connect 0 2> /dev/null

    systemctl daemon-reload
    systemctl restart rabbitmq-server.service
    systemctl restart httpd.service

    rm -rf /%{swdir}/%{name} /var/run/%{name} /var/log/%{name}

    userdel --force %{name} 2> /dev/null; true
    groupdel %{name} 2> /dev/null; true
fi

# on upgrade
if [ "$1" == "1" ]; then
    systemctl daemon-reload
    systemctl restart rabbitmq-server.service
    systemctl restart %{name}-celery.service
    systemctl restart httpd.service
fi


%changelog
