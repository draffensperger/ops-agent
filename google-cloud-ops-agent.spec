Name: google-cloud-ops-agent
Version: %{package_version}
Release: 1%{?dist}
Summary: Google Cloud Ops Agent
Packager: Google Cloud Ops Agent <google-cloud-ops-agent@google.com>
License: ASL 2.0
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The Google Cloud Ops Agent collects metrics and logs from the system.

%define _prefix /opt/%{name}
%define _confdir /etc/%{name}

%prep

%install
cd %{_sourcedir}
DESTDIR="%{buildroot}" ./build.sh

%files
%config %{_confdir}/config.yaml
# We aren't using %{_libdir} here because that would be lib64 on some platforms,
# but the build.sh script hard-codes lib.
%{_prefix}/lib/fluent-bit/*
%{_prefix}/lib/collectd/*
%{_libexecdir}/generate_config
%{_unitdir}/%{name}*

%changelog