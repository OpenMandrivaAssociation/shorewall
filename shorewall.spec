# compatability macros
#%{?!mkrel:%define mkrel(c:) %{-c:0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*)(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

%{?!_with_unstable: %{error:%(echo -e "\n\n\nYou are building package for a stable release, please see \nhttp://qa.mandrakesoft.com/twiki/bin/view/Main/DistroSpecificReleaseTag\nif you think this is incorrect\n\n\n ")}%(sleep 2)}

%define name shorewall
%define version_major 3.4
%define version_minor 4
%define version %{version_major}.%{version_minor}
%define release %mkrel 1
%define ftp_path ftp://ftp.shorewall.net/pub/shorewall/%{version_major}/%{name}-%{version}

Summary: Shoreline Firewall is an iptables-based firewall for Linux systems
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %ftp_path/%{name}-%{version}.tar.bz2
Source2: %ftp_path/%{version}.sha1sums
Source3: %{name}-init.sh
Source4: %ftp_path/%{name}-docs-html-%{version}.tar.bz2
# %{ftp_path}/errata/firewall
# Source11: shorewall-firewall
License: GPL
Group: System/Servers
URL: http://www.shorewall.net/
BuildArch: noarch
Requires: iptables
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildConflicts: apt-common
Requires(post): rpm-helper
Requires(preun): rpm-helper

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

%package doc
Summary:  Firewall scripts
Group:    System/Servers

%description doc 
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

This package contains the docs.

%prep
%setup -q -n %{name}-%{version}

install %SOURCE3 init.sh
tar xjf %SOURCE4

# (blino) enable startup (new setting as of 2.1.3)
perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=Yes/' %{name}.conf
# Keep synced with net.ipv4.ip_forward var in /etc/sysctl.conf
perl -pi -e 's/IP_FORWARDING=.*/IP_FORWARDING=Keep/' %{name}.conf
# blank Internal option 
#perl -pi -e 's/TC_ENABLED=Internal/TC_ENABLED=/' %{name}.conf

mv -f $RPM_BUILD_DIR/%{name}-%{version}/shorewall-docs-html-%{version} $RPM_BUILD_DIR/%{name}-%{version}/documentation

%build
find -name CVS -exec rm -fr {} \;
find -name "*~" -exec rm -rf {} \;
find documentation/ -type f -exec chmod 0644 {} \;

%install
rm -rf %{buildroot}
export PREFIX=%{buildroot}
export OWNER=`id -n -u`
export GROUP=`id -n -g`
./install.sh 

#install -m544 %SOURCE11 %{buildroot}%{_datadir}/%{name}/firewall

# Suppress automatic replacement of "echo" by "gprintf" in the shorewall
# startup script by RPM. This automatic replacement is broken.
export DONT_GPRINTIFY=1

install -d -m 0755 $RPM_BUILD_ROOT/%{_initrddir}
mv -f $RPM_BUILD_ROOT/etc/init.d/shorewall $RPM_BUILD_ROOT/%{_initrddir}/shorewall


%clean
rm -rf $RPM_BUILD_ROOT

%post
%_post_service shorewall

%preun
%_preun_service shorewall
if [ $1 = 0 ] ; then
  %{__rm} -f %{_sysconfdir}/%{name}/startup_disabled
  %{__rm} -f %{_var}/lib/%{name}/*
fi

%files
%defattr(-,root,root)
%doc %attr(-,root,root) COPYING INSTALL changelog.txt releasenotes.txt tunnel ipsecvpn Samples
%attr(700,root,root) %dir /etc/shorewall
%attr(750,root,root) %{_initrddir}/shorewall

%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(0640,root,root) %{_datadir}/%{name}/*
%attr(0700,root,root) %dir %{_var}/lib/%{name}
%attr(540,root,root) /sbin/shorewall
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*

%files doc 
%doc %attr(-,root,root) documentation/*
