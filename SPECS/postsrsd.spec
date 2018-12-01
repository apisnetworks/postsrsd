%bcond apparmor 0
%bcond selinux 0
%bcond init systemd

Name: postsrsd		
Version:  1.4-b474f23
Release:	1%{?dist}
Summary:	SRS daemon for Postfix

Group:		System Environment/Daemons
License:	GPL-2.0
URL:		  https://github.com/roehling/postsrsd
Source0:	https://github.com/roehling/postsrsd/archive/%{version}.tar.gz

BuildRequires: cmake	
Requires:	postfix, systemd

%description 
PostSRSd provides the Sender Rewriting Scheme (SRS) via TCP-based lookup tables 
for Postfix. SRS is needed if your mail server acts as forwarder.

%prep
%setup -q


%build
%cmake -D
%configure
make %{?_smp_mflags}


%install
%makeinstall_std -C build


%files
%doc



%changelog

