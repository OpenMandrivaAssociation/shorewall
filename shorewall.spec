%define version_major 4.0
%define version_minor 8
%define version %{version_major}.%{version_minor}
%define shell_ver %{version}
%define perl_ver %{version}
%define ftp_path ftp://ftp.shorewall.net/pub/shorewall/%{version_major}/%{name}-%{version}

Summary:	Iptables-based firewall for Linux systems
Name:		shorewall
Version:	%{version}
Release:	%mkrel 3
License:	GPLv2+
Group:		System/Servers
URL:		http://www.shorewall.net/
Source0:	%ftp_path/%{name}-common-%{version}.tar.bz2
Source1:	%ftp_path/%{name}-lite-%{version}.tar.bz2
Source2:	%ftp_path/%{name}-perl-%{perl_ver}.tar.bz2
Source3:	%ftp_path/%{name}-shell-%{shell_ver}.tar.bz2
Source4:	%ftp_path/%{name}-docs-html-%{version}.tar.bz2
Source5:	%ftp_path/%{version}.sha1sums
Patch0:		shorewall-common-4.0.7-init-script.patch
Patch1:		shorewall-lite-4.0.7-init-script.patch
Requires:	%{name}-common = %{version}-%{release}
Requires:	%{name}-perl = %{version}-%{release}
BuildConflicts:	apt-common
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

%package common
Summary:	Common shorewall files
Group:		System/Servers
Requires:	iptables
Requires:	iproute2
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description common
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

Shorewall offers two alternative firewall compilers, shorewall-perl and
shorewall-shell. The shorewall-perl compilers is suggested for new installed
systems and shorewall-shell is provided for backwards compatibility and smooth
legacy system upgrades because shorewall perl is not fully compatible with
all legacy configurations.

%package lite
Summary:	Lite version of shorewall
Group:		System/Servers
Requires:	%{name}-common = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description lite
Shorewall Lite is a companion product to Shorewall that allows network
administrators to centralize the configuration of Shorewall-based firewalls.

%package perl
Summary:	Perl compiler for shorewall
Group:		System/Servers
Requires:	%{name}-common = %{version}-%{release}
Requires:	perl
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description perl
Shorewall-perl is a part of Shorewall that allows faster compilation and
execution than the legacy shorewall-shell compiler.

%package shell
Summary:	Shell compiler for shorewall
Group:		System/Servers
Requires:	%{name}-common = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun): rpm-helper

%description shell
Shorewall-shell is a part of Shorewall that allows running shorewall with
legacy configurations. Shorewall-perl is the preferred compiler, please use
it for new installations.

%package doc
Summary:	Firewall scripts
Group:		System/Servers

%description doc 
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

This package contains the docs.

%prep
%setup -q -c -n %{name}-%{version}
%setup -q -T -D -a 1
%setup -q -T -D -a 2
%setup -q -T -D -a 3
%setup -q -T -D -a 4

pushd %{name}-common-%{version}
%patch0 -p1 -b .init
popd

pushd %{name}-lite-%{version}
%patch1 -p1 -b .initlite
popd

%build
# (tpg) we do nothing here

%install
rm -rf %{buildroot}
export PREFIX=%{buildroot}
export OWNER=`id -n -u`
export GROUP=`id -n -g`
export DEST=%{_initrddir}
export CONFDIR=%{_sysconfdir}/%{name}

pushd %{name}-common-%{version}
# (blino) enable startup (new setting as of 2.1.3)
perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=Yes/' %{name}.conf

# Keep synced with net.ipv4.ip_forward var in /etc/sysctl.conf
perl -pi -e 's/IP_FORWARDING=.*/IP_FORWARDING=Keep/' %{name}.conf

# blank Internal option 
perl -pi -e 's/TC_ENABLED=Internal/TC_ENABLED=/' %{name}.conf

# (tpg) use perl compiler
perl -pi -e 's/SHOREWALL_COMPILER=.*/SHOREWALL_COMPILER=perl/' %{name}.conf

# (tpg) do the optimizations
perl -pi -e 's/OPTIMIZE=.*/OPTIMIZE=1/' %{name}.conf

# (tpg) set config path
perl -pi -e 's#CONFIG_PATH=.*#CONFIG_PATH=%{_sysconfdir}/%{name}#' configpath

# let's do the install
./install.sh -n

popd

pushd %{name}-lite-%{version}
./install.sh -n
popd

pushd %{name}-perl-%{perl_ver}
./install.sh -n
popd

pushd %{name}-shell-%{shell_ver}
./install.sh -n
popd

# Suppress automatic replacement of "echo" by "gprintf" in the shorewall
# startup script by RPM. This automatic replacement is broken.
export DONT_GPRINTIFY=1

#(tpg) looks like these files are needed
install -d %{buildroot}/%{_localstatedir}/lib/shorewall
install -d %{buildroot}/%{_localstatedir}/lib/shorewall-lite
touch %{buildroot}/%{_localstatedir}/shorewall/{chains,nat,proxyarp,restarted,zones,restore-base,restore-tail,state,.modules,.modulesdir,.iptables-restore-input,.start,.restart,.restore}
touch %{buildroot}/%{_localstatedir}/shorewall-lite/firewall

%clean
rm -rf %{buildroot}

%post common
%_post_service shorewall

%create_ghostfile %{_localstatedir}/shorewall/chains root root 644
%create_ghostfile %{_localstatedir}/shorewall/nat root root 644
%create_ghostfile %{_localstatedir}/shorewall/proxyarp root root 644
%create_ghostfile %{_localstatedir}/shorewall/restarted root root 644
%create_ghostfile %{_localstatedir}/shorewall/zones root root 644
%create_ghostfile %{_localstatedir}/shorewall/restore-base root root 644
%create_ghostfile %{_localstatedir}/shorewall/restore-tail root root 644
%create_ghostfile %{_localstatedir}/shorewall/state root root 644
%create_ghostfile %{_localstatedir}/shorewall/.modules root root 644
%create_ghostfile %{_localstatedir}/shorewall/.modulesdir root root 644
%create_ghostfile %{_localstatedir}/shorewall/.iptables-restore-input root root 644
%create_ghostfile %{_localstatedir}/shorewall/.restart root root 700
%create_ghostfile %{_localstatedir}/shorewall/.restore root root 700
%create_ghostfile %{_localstatedir}/shorewall/.start root root 700

%preun common
%_preun_service shorewall
if [ $1 = 0 ] ; then
  %{__rm} -f %{_sysconfdir}/%{name}/startup_disabled
  %{__rm} -f %{_var}/lib/%{name}/*
fi

%post lite
%_post_service shorewall-lite

%create_ghostfile %{_localstatedir}/shorewall-lite/firewall

%preun lite
%_preun_service shorewall-lite

%files
%defattr(-,root,root)

%files common
%defattr(-,root,root)
%doc %{name}-common-%{version}/{changelog.txt,releasenotes.txt,tunnel,ipsecvpn,Samples}
%dir %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%ghost %dir %attr(755,root,root) %{_localstatedir}/shorewall
%ghost %{_localstatedir}/shorewall/*
%ghost %{_localstatedir}/shorewall/.*
%attr(700,root,root) %{_initrddir}/shorewall
%config(noreplace) %{_sysconfdir}/%{name}/*
%attr(755,root,root) /sbin/shorewall
%{_datadir}/shorewall/action*
%exclude %{_datadir}/shorewall/configfiles/*
%{_datadir}/shorewall/configpath
%{_datadir}/shorewall/firewall
%{_datadir}/shorewall/functions
%{_datadir}/shorewall/lib.*
%{_datadir}/shorewall/macro.*
%{_datadir}/shorewall/modules
%{_datadir}/shorewall/rfc1918
%{_datadir}/shorewall/version
%{_datadir}/shorewall/wait4ifup
%{_mandir}/man5/shorewall-accounting.5.*
%{_mandir}/man5/shorewall-actions.5.*
%{_mandir}/man5/shorewall-blacklist.5.*
%{_mandir}/man5/shorewall-ecn.5.*
%{_mandir}/man5/shorewall-exclusion.5.*
%{_mandir}/man5/shorewall-hosts.5.*
%{_mandir}/man5/shorewall-interfaces.5.*
%{_mandir}/man5/shorewall-maclist.5.*
%{_mandir}/man5/shorewall-masq.5.*
%{_mandir}/man5/shorewall-modules.5.*
%{_mandir}/man5/shorewall-nat.5.*
%{_mandir}/man5/shorewall-nesting.5.*
%{_mandir}/man5/shorewall-netmap.5.*
%{_mandir}/man5/shorewall-params.5.*
%{_mandir}/man5/shorewall-policy.5.*
%{_mandir}/man5/shorewall-providers.5.*
%{_mandir}/man5/shorewall-proxyarp.5.*
%{_mandir}/man5/shorewall-rfc1918.5.*
%{_mandir}/man5/shorewall-route_rules.5.*
%{_mandir}/man5/shorewall-routestopped.5.*
%{_mandir}/man5/shorewall-rules.5.*
%{_mandir}/man5/shorewall-tcclasses.5.*
%{_mandir}/man5/shorewall-tcdevices.5.*
%{_mandir}/man5/shorewall-tcrules.5.*
%{_mandir}/man5/shorewall-tos.5.*
%{_mandir}/man5/shorewall-tunnels.5.*
%{_mandir}/man5/shorewall-vardir.5.*
%{_mandir}/man5/shorewall-zones.5.*
%{_mandir}/man5/shorewall.conf.5.*
%{_mandir}/man8/shorewall.8.*

%files lite
%defattr(-,root,root)
%doc %{name}-lite-%{version}/*.txt
%dir %{_datadir}/%{name}-lite
%ghost %dir %attr(755,root,root) %{_localstatedir}/shorewall-lite
%ghost %{_localstatedir}/shorewall-lite/*
%ghost %{_localstatedir}/shorewall-lite/.*
%attr(700,root,root) %{_initrddir}/shorewall-lite
%config(noreplace) %{_sysconfdir}/%{name}-lite/*
%attr(755,root,root) /sbin/shorewall-lite
%{_datadir}/shorewall-lite/configpath
%{_datadir}/shorewall-lite/functions
%{_datadir}/shorewall-lite/lib.*
%{_datadir}/shorewall-lite/modules
%{_datadir}/shorewall-lite/shorecap
%{_datadir}/shorewall-lite/version
%{_datadir}/shorewall-lite/wait4ifup
%{_mandir}/man5/shorewall-lite*
%{_mandir}/man8/shorewall-lite*

%files perl
%defattr(-,root,root)
%doc %{name}-perl-%{perl_ver}/*.txt
%dir %{_datadir}/%{name}-perl
%dir %{_datadir}/%{name}-perl/Shorewall
%{_datadir}/%{name}-perl/Shorewall/*.pm
%{_datadir}/%{name}-perl/compiler.pl
%{_datadir}/%{name}-perl/prog.footer
%{_datadir}/%{name}-perl/prog.functions
%{_datadir}/%{name}-perl/prog.header
%{_datadir}/%{name}-perl/version

%files shell
%defattr(-,root,root)
%doc %{name}-shell-%{shell_ver}/*.txt
%dir %{_datadir}/%{name}-shell
%{_datadir}/%{name}-shell/compiler
%{_datadir}/%{name}-shell/lib.*
%{_datadir}/%{name}-shell/prog.*
%{_datadir}/%{name}-shell/version

%files doc 
%defattr(-,root,root)
%doc %{name}-docs-html-%{version}/*
