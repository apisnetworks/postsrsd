%bcond_with apparmor
%bcond_with selinux

%define init systemd
%define postsrsd_user nobody
%define chroot_dir /usr/lib/postsrsd

Name: postsrsd		
Version:  1.12
Release:	20240611.0.ga06dc34%{?dist}
Summary:	SRS daemon for Postfix

Group:		System Environment/Daemons
License:	GPL-2.0
URL:		  https://github.com/roehling/postsrsd
Source0:	https://github.com/roehling/postsrsd/archive/postsrsd-%{version}.tar.bz2

BuildRequires: cmake	
Requires:	postfix, systemd

%description 
PostSRSd provides the Sender Rewriting Scheme (SRS) via TCP-based lookup tables 
for Postfix. SRS is needed if your mail server acts as forwarder.

%prep
%setup -q


%build
BARGS="-DCMAKE_INSTALL_PREFIX=/usr -DCHROOT_DIR=%{chroot_dir}"
%if %{with apparmor}
	BARGS="${BARGS} -DUSE_APPARMOR=ON"
%endif
%if %{with selinux}
	BARGS="${BARGS} -DUSE_SELINUX=ON"
%endif
mkdir _build && cd _build
%cmake .. ${BARGS} -DINIT_FLAVOR=%{init}
%make_build


%install
%make_install

%check
ctest -V %{?_smp_mflags}


%files
%defattr(0644, root, root)
%config(noreplace) /etc/default/postsrsd
%attr(0600, %{postsrsd_user}, root) %{_sysconfdir}/postsrsd.secret
%{_sysconfdir}/systemd/system/postsrsd.service
%attr(0755, root, root) %{chroot_dir}
%attr(0755, root, root) %{_sbindir}/postsrsd
%attr(0755, root, root) %{_datadir}/%{name}/postsrsd-systemd-launcher

%doc
%defattr(0644, root, root)
%dir %attr(0755, root, root) %{_docdir}/postsrsd
%{_docdir}/postsrsd/README.md
%{_docdir}/postsrsd/README_UPGRADE.md
%{_docdir}/postsrsd/main.cf.ex

%posttrans
/bin/systemctl try-restar postsrsd.service >/dev/null 2>&1 || :

%changelog
