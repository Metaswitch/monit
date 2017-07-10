Name: monit
Summary: Process monitor and restart utility
Version: 5.18.1
Release: 1
Group: Utilities/Console
BuildRoot: %{_tmppath}/%{name}-buildroot
License: Metaswitch proprietary

%{!?_with_ssl: %{!?_without_ssl: %define _with_ssl --with-ssl}}
%{?_with_ssl:BuildRequires: openssl-devel}

%{!?_with_pam: %{!?_without_pam: %define _with_pam --with-pam}}
%{?_with_pam:BuildRequires: pam-devel}

%description
Monit is a utility for managing and monitoring processes,
files, directories and filesystems on a Unix system. Monit conducts
automatic maintenance and repair and can execute meaningful causal
actions in error situations.

%prep
%setup

%build
%configure \
        %{?_with_ssl} \
        %{?_without_ssl} \
        %{?_with_pam} \
        %{?_without_pam}
make %{?_smp_mflags}

%install
if [ -d %{buildroot} ] ; then
  rm -rf %{buildroot}
fi

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}/etc/init.d
install -m 755 monit %{buildroot}%{_bindir}/monit
install -m 644 monit.1 %{buildroot}%{_mandir}/man1/monit.1
install -m 600 monitrc %{buildroot}/etc/monitrc
install -m 755 system/startup/rc.monit %{buildroot}/etc/init.d/%{name}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 = 0 ]; then
   /etc/init.d/%{name} stop >/dev/null 2>&1
   /sbin/chkconfig --del %{name}
fi

%clean
if [ -d %{buildroot} ] ; then
  rm -rf %{buildroot}
fi

%files
%defattr(-,root,root)
%doc COPYING
%config(noreplace) /etc/monitrc
%config /etc/init.d/%{name}
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
