Name:		argo-probe-eosccore-helpdesk
Version:	1.0.1
Release:	1%{?dist}
Summary:	Monitoring scripts that check the functionalities of HELPDESK
License:	GPLv3+
Packager:	Themis Zamani <themiszamani@gmail.com>

Source:		%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}
AutoReqProv:    no
Requires:       python-requests, python2-jsonschema

%description
Nagios probe to check functionality of HELPDESK service

%prep
%setup -q

%define _unpackaged_files_terminate_build 0

%install
install -d %{buildroot}/%{_libexecdir}/argo/probes/eosccore-helpdesk
install -m 755 check_healthcheck.py %{buildroot}/%{_libexecdir}/argo/probes/eosccore-helpdesk/check_healthcheck.py

%files
%dir /%{_libexecdir}/argo
%dir /%{_libexecdir}/argo/probes/
%dir /%{_libexecdir}/argo/probes/eosccore-helpdesk

%attr(0755,root,root) /%{_libexecdir}/argo/probes/eosccore-helpdesk/check_healthcheck.py

%changelog
* Tue May 24 2022 Katarina Zailac <katarina.zailac@gmail.com> - 1.0.1-1
- ARGO-3828 Improve probe argo-probe-eosccore-helpdesk
* Tue May 10 2022 Themis Zamani <themiszamani@gmail.com> - 1.0
- Initial version of the package.
