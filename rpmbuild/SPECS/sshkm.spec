Name:		sshkm
Version:	0.1.7
Release:	2%{?dist}
Summary:	SSHKM
Group:		Applications/System
License:	GNU General Public License v3 (GPLv3)
URL:		https://github.com/sshkm/django-sshkm
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	gcc, python, python-virtualenv, python-devel, python-pip, mariadb-devel, postgresql-devel, openldap-devel, httpd-devel, sqlite, rabbitmq-server, httpd, mod_wsgi
Requires:	python, python-virtualenv, sqlite, rabbitmq-server, httpd, mod_wsgi
AutoReqProv:    no

%description
A Django based ssh-key management tool


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
id -g %{name} &>/dev/null || groupadd %{name}
id -u %{name} &>/dev/null || useradd -g %{name} -M -s /sbin/nologin %{name}
mkdir -p /var/run/%{name}/celery
mkdir -p /var/log/%{name}/celery
chown %{name}:%{name} /var/log/%{name}/celery /var/run/%{name}/celery

chown -R %{name} /%{swdir}/%{name}/lib/python*/site-packages/%{name}

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
