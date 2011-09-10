%define debug_package %{nil}

%define version_major 4.4
%define version_minor 23.1
%define version %{version_major}.%{version_minor}
%define version_main %{version}
%define version_lite %{version}
%define ipv6_ver %{version}
%define ipv6_lite_ver %{version}
%define sha1sums_ver %{version_main}
%define ftp_path ftp://ftp.shorewall.net/pub/shorewall/%{version_major}/%{name}-%{version}

%define name6 %{name}6

Summary:	Iptables-based firewall for Linux systems
Name:		shorewall
Version:	%{version}
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Servers
URL:		http://www.shorewall.net/
Source0:	%ftp_path/%{name}-%{version_main}.tar.bz2
Source1:	%ftp_path/%{name}-lite-%{version_lite}.tar.bz2
Source2:	%ftp_path/%{name}-docs-html-%{version}.tar.bz2
Source3:	%ftp_path/%{name6}-%{ipv6_ver}.tar.bz2
Source4:	%ftp_path/%{name6}-lite-%{ipv6_lite_ver}.tar.bz2
Source5:	%ftp_path/%{sha1sums_ver}.sha1sums
Patch0:		%{name}-common-4.2.5-init-script.patch
Patch1:		%{name}-lite-4.2.5-init-script.patch
Patch2:		%{name6}-4.2.5-init-script.patch
Patch3:		%{name6}-lite-4.2.5-init-script.patch
Requires:	iptables >= 1.4.1
Requires:	iproute2
Requires:	dash
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Conflicts:	shorewall < 4.0.7-1
BuildConflicts:	apt-common
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
# since shorewall 4.4 we do not have common, shell and perl modules anymore
Obsoletes:	shorewall-common
Obsoletes:	shorewall-perl
Obsoletes:	shorewall-shell

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

%package ipv6
Summary:	IPv6 capable Shorewall
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Requires:	iptables-ipv6
Requires:	iproute2
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description ipv6
An IPv6 enabled and capable Shoreline Firewall.

%package ipv6-lite
Summary:	Lite version of ipv6 shorewall
Group:		System/Servers
Requires:	%{name}-ipv6 = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description ipv6-lite
Shorewall IPv6 Lite is a companion product to Shorewall IPv6 that allows 
network administrators to centralize the configuration of Shorewall-based
firewalls.

%package lite
Summary:	Lite version of shorewall
Group:		System/Servers
Requires:	%{name} = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description lite
Shorewall Lite is a companion product to Shorewall that allows network
administrators to centralize the configuration of Shorewall-based firewalls.

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

pushd %{name}-%{version_main}
%patch0 -p1 -b .init
popd

pushd %{name}-lite-%{version_lite}
%patch1 -p1 -b .initlite
popd

pushd %{name6}-%{ipv6_ver}
%patch2 -p1 -b .init6
popd

pushd %{name6}-lite-%{ipv6_lite_ver}
%patch3 -p1 -b .init6lite
popd

%build
# (tpg) we do nothing here

# (tpg) add comment to the configfiles
for i in $(find -L configfiles  -type f);
do echo "#LAST LINE -- DO NOT REMOVE" >> $i;
done

%install
rm -rf %{buildroot}
export PREFIX=%{buildroot}
export OWNER=`id -n -u`
export GROUP=`id -n -g`
export DEST=%{_initrddir}

pushd %{name}-%{version_main}
export CONFDIR=%{_sysconfdir}/%{name}
# (blino) enable startup (new setting as of 2.1.3)
perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=Yes/' configfiles/%{name}.conf

# Keep synced with net.ipv4.ip_forward var in /etc/sysctl.conf
perl -pi -e 's/IP_FORWARDING=.*/IP_FORWARDING=Keep/' configfiles/%{name}.conf

# blank Internal option 
perl -pi -e 's/TC_ENABLED=Internal/TC_ENABLED=/' configfiles/%{name}.conf

# (tpg) use perl compiler
perl -pi -e 's/SHOREWALL_COMPILER=.*/SHOREWALL_COMPILER=perl/' configfiles/%{name}.conf

# (tpg) do the optimizations
perl -pi -e 's/OPTIMIZE=.*/OPTIMIZE=1/' configfiles/%{name}.conf

# (tpg) enable IPv6
perl -pi -e 's#DISABLE_IPV6=.*#DISABLE_IPV6=No#' configfiles/%{name}.conf

# (tpg) set config path
perl -pi -e 's#CONFIG_PATH=.*#CONFIG_PATH=configfiles/%{/g_sysconfdir}/%{name}#' configpath

# let's do the install
./install.sh
popd

#(tpg) IPv6
pushd %{name6}-%{ipv6_ver}
# (blino) enable startup (new setting as of 2.1.3)
perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=Yes/' %{name6}.conf
# Keep synced with net.ipv4.ip_forward var in /etc/sysctl.conf
perl -pi -e 's/IP_FORWARDING=.*/IP_FORWARDING=Keep/' %{name6}.conf

./install.sh
popd

pushd %{name6}-lite-%{ipv6_lite_ver}
./install.sh
popd

pushd %{name}-lite-%{version_lite}
./install.sh
popd

# Suppress automatic replacement of "echo" by "gprintf" in the shorewall
# startup script by RPM. This automatic replacement is broken.
export DONT_GPRINTIFY=1

#(tpg) looks like these files are needed
touch %{buildroot}/%{_var}/lib/shorewall/{chains,nat,proxyarp,restarted,zones,restore-base,restore-tail,state,.modules,.modulesdir,.iptables-restore-input,.start,.restart,.restore}
touch %{buildroot}/%{_var}/lib/shorewall-lite/firewall

#(tpg) ipv6
touch %{buildroot}/%{_var}/lib/%{name6}/{chains,restarted,zones,restore-base,restore-tail,state,.modules,.modulesdir,.iptables-restore-input,.start,.restart,.restore}
touch %{buildroot}/%{_var}/lib/%{name6}-lite/firewall

#(tpg) remove hash-bang
find %{buildroot} -name "lib.*" -exec sed -i -e '/\#\!\/bin\/sh/d' {} \;

# (tpg) let's use dash everywhere!
find %{buildroot} -type f -exec sed -i -e 's@/bin/sh@/bin/dash@' {} \;

# add information about 4.4.0 upgrade
cat > README.4.4.0.upgrade.urpmi << EOF
As of shorewall 4.4.0, the shorewall-common and shorewall-perl packages
were merged into a single shorewall package. Other notable changes in 4.4.0
version are:
 - The support for shorewall-shell has been discontinued
 - Support for SAME target in /etc/shorewall/masq and /etc/shorewall/rules
   has been removed.
 - Support for norfc1918 and RFC1918_STRICT have been removed.
 - The name 'any' is now reserved and may not be used as a zone name.

If you were relying on those options, please review your shorewall
configuration. Refer to the /usr/share/doc/shorewall/releasenotes.txt file
for further instructions.
EOF

# due to the removal of the %%exclude macro...
rm -rf %{buildroot}%{_datadir}/%{name6}/configfiles
rm -rf %{buildroot}%{_datadir}/shorewall/configfiles

%clean
rm -rf %{buildroot}

%post
%_post_service shorewall

%create_ghostfile %{_var}/lib/%{name}/chains root root 644
%create_ghostfile %{_var}/lib/%{name}/nat root root 644
%create_ghostfile %{_var}/lib/%{name}/proxyarp root root 644
%create_ghostfile %{_var}/lib/%{name}/restarted root root 644
%create_ghostfile %{_var}/lib/%{name}/zones root root 644
%create_ghostfile %{_var}/lib/%{name}/restore-base root root 644
%create_ghostfile %{_var}/lib/%{name}/restore-tail root root 644
%create_ghostfile %{_var}/lib/%{name}/state root root 644
%create_ghostfile %{_var}/lib/%{name}/.modules root root 644
%create_ghostfile %{_var}/lib/%{name}/.modulesdir root root 644
%create_ghostfile %{_var}/lib/%{name}/.iptables-restore-input root root 644
%create_ghostfile %{_var}/lib/%{name}/.restart root root 700
%create_ghostfile %{_var}/lib/%{name}/.restore root root 700
%create_ghostfile %{_var}/lib/%{name}/.start root root 700

%preun
%_preun_service %{name}
if [ $1 = 0 ] ; then
  %{__rm} -f %{_sysconfdir}/%{name}/startup_disabled
  %{__rm} -f %{_var}/lib/%{name}/*
fi

%post lite
%_post_service %{name}-lite
%create_ghostfile %{_var}/lib/%{name}-lite/firewall root root 644

%preun lite
%_preun_service %{name}-lite

%post ipv6
%_post_service %{name6}

%create_ghostfile %{_var}/lib/%{name6}/chains root root 644
%create_ghostfile %{_var}/lib/%{name6}/restarted root root 644
%create_ghostfile %{_var}/lib/%{name6}/zones root root 644
%create_ghostfile %{_var}/lib/%{name6}/restore-base root root 644
%create_ghostfile %{_var}/lib/%{name6}/restore-tail root root 644
%create_ghostfile %{_var}/lib/%{name6}/state root root 644
%create_ghostfile %{_var}/lib/%{name6}/.modules root root 644
%create_ghostfile %{_var}/lib/%{name6}/.modulesdir root root 644
%create_ghostfile %{_var}/lib/%{name6}/.iptables-restore-input root root 644
%create_ghostfile %{_var}/lib/%{name6}/.restart root root 700
%create_ghostfile %{_var}/lib/%{name6}/.restore root root 700
%create_ghostfile %{_var}/lib/%{name6}/.start root root 700

%preun ipv6
%_preun_service %{name6}
if [ $1 = 0 ] ; then
  %{__rm} -f %{_sysconfdir}/%{name6}/startup_disabled
  %{__rm} -f %{_var}/lib/%{name6}/*
fi

%post ipv6-lite
%_post_service %{name6}-lite
%create_ghostfile %{_var}/lib/%{name6}-lite/firewall root root 644

%preun ipv6-lite
%_preun_service %{name6}-lite

%files
%defattr(-,root,root)
%doc README.4.4.0.upgrade.urpmi %{name}-%{version_main}/{changelog.txt,releasenotes.txt,Samples}
%dir %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%dir %attr(755,root,root) %{_var}/lib/%{name}
%ghost %{_var}/lib/%{name}/*
%ghost %{_var}/lib/%{name}/.??*
%config %{_sysconfdir}/logrotate.d/%{name}
%attr(700,root,root) %{_initrddir}/%{name}
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(755,root,root) /sbin/%{name}
%{_datadir}/%{name}/action*
%{_datadir}/%{name}/configpath
%{_datadir}/%{name}/functions
%{_datadir}/%{name}/helpers
%{_datadir}/%{name}/lib.*
%{_datadir}/%{name}/macro.*
%{_datadir}/%{name}/modules*
%{_datadir}/%{name}/version
%{_datadir}/%{name}/wait4ifup
%{_datadir}/%{name}/getparams
%{_mandir}/man5/%{name}-accounting.5.*
%{_mandir}/man5/%{name}-actions.5.*
%{_mandir}/man5/%{name}-blacklist.5.*
%{_mandir}/man5/%{name}-ecn.5.*
%{_mandir}/man5/%{name}-exclusion.5.*
%{_mandir}/man5/%{name}-hosts.5.*
%{_mandir}/man5/%{name}-interfaces.5.*
%{_mandir}/man5/%{name}-maclist.5.*
%{_mandir}/man5/%{name}-masq.5.*
%{_mandir}/man5/%{name}-modules.5.*
%{_mandir}/man5/%{name}-nat.5.*
%{_mandir}/man5/%{name}-nesting.5.*
%{_mandir}/man5/%{name}-notrack.5.*
%{_mandir}/man5/%{name}-netmap.5.*
%{_mandir}/man5/%{name}-params.5.*
%{_mandir}/man5/%{name}-policy.5.*
%{_mandir}/man5/%{name}-providers.5.*
%{_mandir}/man5/%{name}-proxyarp.5.*
%{_mandir}/man5/%{name}-route_rules.5.*
%{_mandir}/man5/%{name}-routestopped.5.*
%{_mandir}/man5/%{name}-rules.5.*
%{_mandir}/man5/%{name}-tcclasses.5.*
%{_mandir}/man5/%{name}-tcinterfaces.5.*
%{_mandir}/man5/%{name}-tcpri.5.*
%{_mandir}/man5/%{name}-tcdevices.5.*
%{_mandir}/man5/%{name}-tcfilters.5.*
%{_mandir}/man5/%{name}-tcrules.5.*
%{_mandir}/man5/%{name}-tos.5.*
%{_mandir}/man5/%{name}-tunnels.5.*
%{_mandir}/man5/%{name}-vardir.5.*
%{_mandir}/man5/%{name}-zones.5.*
%{_mandir}/man5/%{name}.conf.5.*
%{_mandir}/man5/%{name}-ipsets.5*
%{_mandir}/man5/%{name}-routes.5*
%{_mandir}/man5/%{name}-secmarks.5*
%{_mandir}/man8/%{name}.8.*
%{_mandir}/man8/%{name}-init.8.*
%dir %{_datadir}/shorewall/Shorewall
%{_datadir}/shorewall/Shorewall/*.pm
%{_datadir}/shorewall/compiler.pl
%{_datadir}/shorewall/prog.footer
%{_datadir}/shorewall/prog.header

%files ipv6
%defattr(-,root,root)
%doc %{name6}-%{ipv6_ver}/{changelog.txt,releasenotes.txt,tunnel,ipsecvpn,Samples6}
%dir %{_sysconfdir}/%{name6}
%dir %{_datadir}/%{name6}
%dir %attr(755,root,root) %{_var}/lib/%{name6}
%ghost %{_var}/lib/%{name6}/*
%ghost %{_var}/lib/%{name6}/.??*
%attr(700,root,root) %{_initrddir}/%{name6}
%config(noreplace) %{_sysconfdir}/%{name6}/*
%config %{_sysconfdir}/logrotate.d/%{name6}
%attr(755,root,root) /sbin/%{name6}
%{_datadir}/%{name6}/action*
%{_datadir}/%{name}/prog.footer6
%{_datadir}/%{name}/prog.header6
%{_datadir}/%{name6}/configpath
%{_datadir}/%{name6}/functions
%{_datadir}/%{name6}/helpers
%{_datadir}/%{name6}/lib.*
%{_datadir}/%{name6}/macro.*
%{_datadir}/%{name6}/modules*
%{_datadir}/%{name6}/version
%{_datadir}/%{name6}/wait4ifup
%{_mandir}/man5/%{name6}-accounting.5.*
%{_mandir}/man5/%{name6}-actions.5.*
%{_mandir}/man5/%{name6}-blacklist.5.*
%{_mandir}/man5/%{name6}-exclusion.5.*
%{_mandir}/man5/%{name6}-hosts.5.*
%{_mandir}/man5/%{name6}-interfaces.5.*
%{_mandir}/man5/%{name6}-ipsets.5.*
%{_mandir}/man5/%{name6}-maclist.5.*
%{_mandir}/man5/%{name6}-modules.5.*
%{_mandir}/man5/%{name6}-nesting.5.*
%{_mandir}/man5/%{name6}-notrack.5.*
%{_mandir}/man5/%{name6}-params.5.*
%{_mandir}/man5/%{name6}-policy.5.*
%{_mandir}/man5/%{name6}-providers.5.*
%{_mandir}/man5/%{name6}-route_rules.5.*
%{_mandir}/man5/%{name6}-routestopped.5.*
%{_mandir}/man5/%{name6}-rules.5.*
%{_mandir}/man5/%{name6}-tcclasses.5.*
%{_mandir}/man5/%{name6}-tcdevices.5.*
%{_mandir}/man5/%{name6}-tcinterfaces.5.*
%{_mandir}/man5/%{name6}-tcpri.5.*
%{_mandir}/man5/%{name6}-tcrules.5.*
%{_mandir}/man5/%{name6}-tos.5.*
%{_mandir}/man5/%{name6}-tunnels.5.*
%{_mandir}/man5/%{name6}-vardir.5.*
%{_mandir}/man5/%{name6}-zones.5.*
%{_mandir}/man5/%{name6}.conf.5.*
%{_mandir}/man5/%{name6}-proxyndp.5*
%{_mandir}/man5/%{name6}-routes.5*
%{_mandir}/man5/%{name6}-secmarks.5*
%{_mandir}/man5/%{name6}-tcfilters.5*
%{_mandir}/man8/%{name6}.8.*

%files lite
%defattr(-,root,root)
%doc %{name}-lite-%{version_lite}/*.txt
%dir %{_datadir}/%{name}-lite
%dir %attr(755,root,root) %{_var}/lib/%{name}-lite
%ghost %{_var}/lib/%{name}-lite/*
%attr(700,root,root) %{_initrddir}/%{name}-lite
%config(noreplace) %{_sysconfdir}/%{name}-lite/*
%config %{_sysconfdir}/logrotate.d/%{name}-lite
%attr(755,root,root) /sbin/%{name}-lite
%{_datadir}/%{name}-lite/configpath
%{_datadir}/%{name}-lite/functions
%{_datadir}/%{name}-lite/lib.*
%{_datadir}/%{name}-lite/modules*
%{_datadir}/%{name}-lite/shorecap
%{_datadir}/%{name}-lite/version
%{_datadir}/%{name}-lite/wait4ifup
%{_datadir}/%{name}-lite/helpers
%{_mandir}/man5/%{name}-lite*
%{_mandir}/man8/%{name}-lite*

%files ipv6-lite
%defattr(-,root,root)
%doc %{name6}-lite-%{ipv6_lite_ver}/*.txt
%dir %{_datadir}/%{name6}-lite
%dir %attr(755,root,root) %{_var}/lib/%{name6}-lite
%ghost %{_var}/lib/%{name6}-lite/*
%attr(700,root,root) %{_initrddir}/%{name6}-lite
%config(noreplace) %{_sysconfdir}/%{name6}-lite/*
%config %{_sysconfdir}/logrotate.d/%{name6}-lite
%attr(755,root,root) /sbin/%{name6}-lite
%{_datadir}/%{name6}-lite/configpath
%{_datadir}/%{name6}-lite/functions
%{_datadir}/%{name6}-lite/lib.*
%{_datadir}/%{name6}-lite/modules*
%{_datadir}/%{name6}-lite/shorecap
%{_datadir}/%{name6}-lite/version
%{_datadir}/%{name6}-lite/wait4ifup
%{_datadir}/%{name6}-lite/helpers
%{_mandir}/man5/%{name6}-lite*
%{_mandir}/man8/%{name6}-lite*

%files doc
%defattr(-,root,root)
%doc %{name}-docs-html-%{version}/*
