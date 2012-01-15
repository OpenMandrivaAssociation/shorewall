%define debug_package %{nil}

%define version_major 4.4
%define version_minor 25
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
Group:		System/Configuration/Networking
URL:		http://www.shorewall.net/
Source0:	%ftp_path/%{name}-%{version_main}.tar.bz2
Source1:	%ftp_path/%{name}-lite-%{version_lite}.tar.bz2
Source2:	%ftp_path/%{name}-docs-html-%{version}.tar.bz2
Source3:	%ftp_path/%{name6}-%{ipv6_ver}.tar.bz2
Source4:	%ftp_path/%{name6}-lite-%{ipv6_lite_ver}.tar.bz2
Source5:	%ftp_path/%{name}-init-%{version_main}.tar.bz2
Source6:	%ftp_path/%{sha1sums_ver}.sha1sums
BuildConflicts:	apt-common
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
BuildRequires:	perl
BuildRequires:	systemd-units
# since shorewall 4.4 we do not have common, shell and perl modules anymore
Obsoletes:	shorewall-common
Obsoletes:	shorewall-perl
Obsoletes:	shorewall-shell
Conflicts:	shorewall < 4.0.7-1
Requires:	iptables >= 1.4.1
Requires:	iproute2
Requires:	dash
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(post):	/sbin/chkconfig
Requires(post):	systemd-units
Requires(post):	systemd-sysvinit
Requires(preun):	systemd-units
Requires(postun):	systemd-units

%description
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

%package -n %{name6}
Summary:	IPv6 capable Shorewall
Group:		System/Configuration/Networking
Requires:	%{name} = %{version}-%{release}
Requires:	iptables-ipv6
Requires:	iproute2
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(post):	/sbin/chkconfig
Requires(post):	systemd-units
Requires(post):	systemd-sysvinit
Requires(preun):	systemd-units
Requires(postun):	systemd-units
Obsoletes:	%{name}-ipv6 < 4.4.24
Provides:	%{name}-ipv6

%description -n %{name6}
An IPv6 enabled and capable Shoreline Firewall.

%package -n %{name6}-lite
Summary:	Lite version of ipv6 shorewall
Group:		System/Configuration/Networking
Requires:	%{name6} = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(post):	/sbin/chkconfig
Requires(post):	systemd-units
Requires(post):	systemd-sysvinit
Requires(preun):	systemd-units
Requires(postun):	systemd-units
Obsoletes:	%{name}-ipv6-lite < 4.4.24
Provides:	%{name}-ipv6-lite

%description -n %{name6}-lite
Shorewall IPv6 Lite is a companion product to Shorewall IPv6 that allows 
network administrators to centralize the configuration of Shorewall-based
firewalls.

%package lite
Summary:	Lite version of shorewall
Group:		System/Configuration/Networking
Requires:	%{name} = %{version}-%{release}
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(post):	/sbin/chkconfig
Requires(post):	systemd-units
Requires(post):	systemd-sysvinit
Requires(preun):	systemd-units
Requires(postun):	systemd-units

%description lite
Shorewall Lite is a companion product to Shorewall that allows network
administrators to centralize the configuration of Shorewall-based firewalls.

%package init
Summary:	Initialization functionality and NetworkManager integration for Shorewall
Group:		System/Configuration/Networking
Requires:	NetworkManager
Requires:	%{name} = %{version}-%{release}
Requires(post):	/sbin/chkconfig
Requires(post):	systemd-units
Requires(post):	systemd-sysvinit
Requires(preun):	systemd-units
Requires(postun):	systemd-units

%description init
This package adds additional initialization functionality to Shorewall in two
ways. It allows the firewall to be closed prior to bringing up network
devices. This insures that unwanted connections are not allowed between the
time that the network comes up and when the firewall is started. It also
integrates with NetworkManager and distribution ifup/ifdown systems to allow
for 'event-driven' startup and shutdown.

%package doc
Summary:	Firewall scripts
Group:		Books/Computer books

%description doc
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

This package contains the docs.

%prep
%setup -q -c -n %{name}-%{version} -T -a0 -a1 -a2 -a3 -a4 -a5

%build
# (tpg) we do nothing here

# (tpg) add comment to the configfiles
for i in $(find -L $(find . -name configfiles -type d)  -type f);
do echo "#LAST LINE -- DO NOT REMOVE" >> $i;
done

%install
rm -rf %{buildroot}
export PREFIX=%{buildroot}
export OWNER=`id -n -u`
export GROUP=`id -n -g`
%if %mdkver >= 201100
export DEST=%{_unitdir}
%else
export DEST=%{_initrddir}
%endif
export CONFDIR=%{_sysconfdir}/%{name}

pushd %{name}-%{version_main}
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

# (tpg) enable AUTOMAKE - skip comilation on start/restart if there were no changes in rules
perl -pi -e 's/AUTOMAKE=.*/AUTOMAKE=Yes/' configfiles/%{name}.conf

popd

#(tpg) IPv6
pushd %{name6}-%{ipv6_ver}
# (blino) enable startup (new setting as of 2.1.3)
perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=Yes/' %{name6}.conf
# Keep synced with net.ipv4.ip_forward var in /etc/sysctl.conf
perl -pi -e 's/IP_FORWARDING=.*/IP_FORWARDING=Keep/' %{name6}.conf

popd

# let's do the install
targets="shorewall shorewall-lite shorewall6 shorewall6-lite shorewall-init"
mkdir -p %{buildroot}%{_unitdir}

for i in $targets; do
    pushd ${i}-%{version}
	./install.sh
	install -m 644 ${i}.service %{buildroot}%{_unitdir}/${i}.service
     popd
done

#(tpg) drop init files
rm -rf %{buildroot}%{_initddir}

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
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -eq 1 ] ; then
    /bin/systemctl enable shorewall.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart shorewall.service >/dev/null 2>&1 || :
fi

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
if [ $1 -eq 0 ] ; then
    /bin/systemctl --no-reload disable shorewall.service > /dev/null 2>&1 || :
    /bin/systemctl stop shorewall.service > /dev/null 2>&1 || :
    %{__rm} -f %{_var}/lib/%{name}/*
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart shorewall.service >/dev/null 2>&1 || :
fi

%triggerun -- shorewall < 4.4.23.1-2
/sbin/chkconfig --del shorewall >/dev/null 2>&1 || :
/bin/systemctl try-restart shorewall.service >/dev/null 2>&1 || :


%post -n %{name}-lite
if [ $1 -eq 1 ] ; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%create_ghostfile %{_var}/lib/%{name}-lite/firewall root root 644

%preun -n %{name}-lite
if [ $1 -eq 0 ] ; then
    /bin/systemctl --no-reload disable shorewall-lite.service > /dev/null 2>&1 || :
    /bin/systemctl stop shorewall-lite.service > /dev/null 2>&1 || :
    %{__rm} -f %{_var}/lib/%{name}-lite/*
fi

%postun -n %{name}-lite
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart shorewall-lite.service >/dev/null 2>&1 || :
fi

%triggerun -- shorewall-lite < 4.4.23.1-2
/sbin/chkconfig --del shorewall-lite >/dev/null 2>&1 || :
/bin/systemctl try-restart shorewall-lite.service >/dev/null 2>&1 || :

%post -n %{name6}
if [ $1 -eq 1 ] ; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

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

%preun -n %{name6}
if [ $1 -eq 0 ] ; then
    /bin/systemctl --no-reload disable shorewall6.service > /dev/null 2>&1 || :
    /bin/systemctl stop shorewall6.service > /dev/null 2>&1 || :
    %{__rm} -f %{_var}/lib/%{name6}/*
fi

%postun -n %{name6}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart shorewall6.service >/dev/null 2>&1 || :
fi

%triggerun -- shorewall-ipv6 < 4.4.23.1-2
/sbin/chkconfig --del shorewall6 >/dev/null 2>&1 || :
/bin/systemctl try-restart shorewall6.service >/dev/null 2>&1 || :

%post -n %{name6}-lite
if [ $1 -eq 1 ] ; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%create_ghostfile %{_var}/lib/%{name6}-lite/firewall root root 644

%preun -n %{name6}-lite
if [ $1 -eq 0 ] ; then
    /bin/systemctl --no-reload disable shorewall6-lite.service > /dev/null 2>&1 || :
    /bin/systemctl stop shorewall6-lite.service > /dev/null 2>&1 || :
    %{__rm} -f %{_var}/lib/%{name6}-lite/*
fi

%postun -n %{name6}-lite
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart shorewall6-lite.service >/dev/null 2>&1 || :
fi

%triggerun -- shorewall-ipv6-lite < 4.4.23.1-2
/sbin/chkconfig --del shorewall6-lite >/dev/null 2>&1 || :
/bin/systemctl try-restart shorewall6-lite.service >/dev/null 2>&1 || :

%post -n %{name}-init
if [ $1 -eq 1 ] ; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun -n %{name}-init
if [ $1 -eq 0 ] ; then
    /bin/systemctl --no-reload disable shorewall-init.service > /dev/null 2>&1 || :
    /bin/systemctl stop shorewall-init.service > /dev/null 2>&1 || :
    %{__rm} -f %{_var}/lib/%{name}-init/*
fi

%postun -n %{name}-init
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl try-restart shorewall-init.service >/dev/null 2>&1 || :
fi

%triggerun -- shorewall-init < 4.4.23.1-2
/sbin/chkconfig --del shorewall-init >/dev/null 2>&1 || :
/bin/systemctl try-restart shorewall-init.service >/dev/null 2>&1 || :

%files
%defattr(-,root,root)
%doc README.4.4.0.upgrade.urpmi %{name}-%{version_main}/{changelog.txt,releasenotes.txt,Samples}
%dir %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%dir %attr(755,root,root) %{_var}/lib/%{name}
%ghost %{_var}/lib/%{name}/*
%ghost %{_var}/lib/%{name}/.??*
%config %{_sysconfdir}/logrotate.d/%{name}
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(755,root,root) /sbin/%{name}
%if %mdkver >= 201100
%{_unitdir}/shorewall.service
%else
%attr(700,root,root) %{_initrddir}/%{name}
%endif
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
%dir %{_datadir}/shorewall/Shorewall
%{_datadir}/shorewall/Shorewall/*.pm
%{_datadir}/shorewall/compiler.pl
%{_datadir}/shorewall/prog.footer
%{_datadir}/shorewall/prog.header

%files -n %{name6}
%defattr(-,root,root)
%doc %{name6}-%{ipv6_ver}/{changelog.txt,releasenotes.txt,tunnel,ipsecvpn,Samples6}
%dir %{_sysconfdir}/%{name6}
%dir %{_datadir}/%{name6}
%dir %attr(755,root,root) %{_var}/lib/%{name6}
%ghost %{_var}/lib/%{name6}/*
%ghost %{_var}/lib/%{name6}/.??*
%config(noreplace) %{_sysconfdir}/%{name6}/*
%config %{_sysconfdir}/logrotate.d/%{name6}
%attr(755,root,root) /sbin/%{name6}
%if %mdkver >= 201100
%{_unitdir}/shorewall6.service
%else
%attr(700,root,root) %{_initrddir}/%{name6}
%endif
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
%{_mandir}/man5/%{name6}-netmap.5.*
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
%config(noreplace) %{_sysconfdir}/%{name}-lite/*
%config %{_sysconfdir}/logrotate.d/%{name}-lite
%attr(755,root,root) /sbin/%{name}-lite
%if %mdkver >= 201100
%{_unitdir}/shorewall-lite.service
%else
%attr(700,root,root) %{_initrddir}/%{name}-lite
%endif
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

%files -n %{name6}-lite
%defattr(-,root,root)
%doc %{name6}-lite-%{ipv6_lite_ver}/*.txt
%dir %{_datadir}/%{name6}-lite
%dir %attr(755,root,root) %{_var}/lib/%{name6}-lite
%ghost %{_var}/lib/%{name6}-lite/*
%config(noreplace) %{_sysconfdir}/%{name6}-lite/*
%config %{_sysconfdir}/logrotate.d/%{name6}-lite
%attr(755,root,root) /sbin/%{name6}-lite
%if %mdkver >= 201100
%{_unitdir}/shorewall6-lite.service
%else
%attr(700,root,root) %{_initrddir}/%{name6}-lite
%endif
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

%files init
%defattr(-,root,root)
%doc shorewall-init-%{version}/{COPYING,changelog.txt,releasenotes.txt}
%{_sysconfdir}/NetworkManager/dispatcher.d/01-shorewall
%config(noreplace) %{_sysconfdir}/sysconfig/shorewall-init
%if %mdkver >= 201100
%{_unitdir}/shorewall-init.service
%else
%attr(700,root,root) %{_initrddir}/%{name}-init
%endif
%{_datadir}/shorewall-init
%{_mandir}/man8/%{name}-init.8.*

%files doc
%defattr(-,root,root)
%doc %{name}-docs-html-%{version}/*
