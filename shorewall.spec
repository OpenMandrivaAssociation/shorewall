%define debug_package %{nil}

%define version_major 4.5
%define version_minor 19
%define version %{version_major}.%{version_minor}
%define version_main %{version}
%define version_lite %{version}
%define ipv6_ver %{version}
%define ipv6_lite_ver %{version}
%define ftp_path ftp://ftp.shorewall.net/pub/shorewall/%{version_major}/%{name}-%{version}

%define name6 %{name}6

Summary:	Iptables-based firewall for Linux systems
Name:		shorewall
Version:	%{version}
Release:	3
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		http://www.shorewall.net/
Source0:	%ftp_path/%{name}-%{version_main}.tar.bz2
Source1:	%ftp_path/%{name}-lite-%{version_lite}.tar.bz2
Source2:	%ftp_path/%{name}-docs-html-%{version}.tar.bz2
Source3:	%ftp_path/%{name6}-%{ipv6_ver}.tar.bz2
Source4:	%ftp_path/%{name6}-lite-%{ipv6_lite_ver}.tar.bz2
Source5:	%ftp_path/%{name}-init-%{version_main}.tar.bz2
Source6:	%ftp_path/%{name}-core-%{version}.tar.bz2
Source100:	shorewall.rpmlintrc
BuildConflicts:	apt-common
BuildArch:	noarch
BuildRequires:	perl
BuildRequires:	systemd-units
BuildRequires:	perl(Digest::SHA1)
# since shorewall 4.4 we do not have common, shell and perl modules anymore
Obsoletes:	shorewall-common < 4.5
Obsoletes:	shorewall-perl < 4.5
Obsoletes:	shorewall-shell < 4.5
Provides:	shorewall-common = %{version}
Provides:	shorewall-perl = %{version}
Provides:	shorewall-shell = %{version}
Conflicts:	shorewall < 4.0.7-1
Requires:	iptables >= 1.4.1
Requires:	iproute2
Requires:	dash
Requires:	%{name}-core = %{EVRD}
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

%package core
Summary:	Shorewall core libraries
Group:		System/Configuration/Networking
Requires:	%{name} = %{EVRD}
Conflicts:	shorewall < 4.5
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description core
An IPv6 enabled and capable Shoreline Firewall.

%package -n %{name6}
Summary:	IPv6 capable Shorewall
Group:		System/Configuration/Networking
Requires:	%{name} = %{EVRD}
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
Provides:	%{name}-ipv6 = %{version}

%description -n %{name6}
An IPv6 enabled and capable Shoreline Firewall.

%package -n %{name6}-lite
Summary:	Lite version of ipv6 shorewall
Group:		System/Configuration/Networking
Requires:	%{name6} = %{EVRD}
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
Requires(post):	/sbin/chkconfig
Requires(post):	systemd-units
Requires(post):	systemd-sysvinit
Requires(preun):	systemd-units
Requires(postun):	systemd-units
Obsoletes:	%{name}-ipv6-lite < 4.4.24
Provides:	%{name}-ipv6-lite = %{version}

%description -n %{name6}-lite
Shorewall IPv6 Lite is a companion product to Shorewall IPv6 that allows 
network administrators to centralize the configuration of Shorewall-based
firewalls.

%package lite
Summary:	Lite version of shorewall
Group:		System/Configuration/Networking
Requires:	%{name} = %{EVRD}
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
Requires:	%{name} = %{EVRD}
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
Requires:	%{name} = %{EVRD}

%description doc
The Shoreline Firewall, more commonly known as "Shorewall", is a Netfilter
(iptables) based firewall that can be used on a dedicated firewall system,
a multi-function gateway/ router/server or on a standalone GNU/Linux system.

This package contains the docs.

%prep
%setup -q -c -n %{name}-%{version} -T -a0 -a1 -a2 -a3 -a4 -a5 -a6

%build
# (tpg) we do nothing here

# (tpg) add comment to the configfiles
for i in $(find -L $(find . -name configfiles -type d)  -type f);
do echo "#LAST LINE -- DO NOT REMOVE" >> $i;
done

%install
export PREFIX=%{buildroot}
export OWNER=`id -n -u`
export GROUP=`id -n -g`
export CONFDIR=%{_sysconfdir}/%{name}
export SYSTEMD=%{_unitdir}
export SBINDIR=%{_sbindir}
export LIBEXEC=%{_libexecdir}
export DESTDIR=%{buildroot}


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
perl -pi -e 's/STARTUP_ENABLED=.*/STARTUP_ENABLED=Yes/' configfiles/%{name6}.conf
# Keep synced with net.ipv4.ip_forward var in /etc/sysctl.conf
perl -pi -e 's/IP_FORWARDING=.*/IP_FORWARDING=Keep/' configfiles/%{name6}.conf

popd

# let's do the install
targets="shorewall-core shorewall shorewall-lite shorewall6 shorewall6-lite shorewall-init"
use_rc="shorewallrc.default"

mkdir -p %{buildroot}%{_unitdir}

for i in $targets; do
    pushd ${i}-%{version}
# (tpg) few corrections
	sed -i -e 's@MANDIR=.*@MANDIR=%{_mandir}@' \
	-e 's@INITDIR=.*@INITDIR=%{_initddir}@' \
	-e 's@SYSCONFDIR=.*@SYSCONFDIR=%{_sysconfdir}/sysconfig@' $use_rc

	./configure.pl
	./install.sh $use_rc
	if [ $i != "%{name}-core" ]; then
	install -m 644 *.service %{buildroot}%{_unitdir}
	fi;
     popd
done ;

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

# (tpg) remove old initscripts
rm -rf %{buildroot}%{_initrddir}

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
%doc README.4.4.0.upgrade.urpmi %{name}-%{version_main}/{changelog.txt,releasenotes.txt,Samples}
%dir %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%dir %attr(755,root,root) %{_var}/lib/%{name}
%ghost %{_var}/lib/%{name}/*
%ghost %{_var}/lib/%{name}/.??*
%config %{_sysconfdir}/logrotate.d/%{name}
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/%{name}/*
%attr(755,root,root) /sbin/%{name}
%{_unitdir}/shorewall.service
%{_datadir}/%{name}/action*
%{_datadir}/%{name}/configpath
%{_datadir}/%{name}/helpers
%{_datadir}/%{name}/lib.cli-std
%{_datadir}/%{name}/lib.core
%{_datadir}/%{name}/macro.*
%{_datadir}/%{name}/modules*
%{_datadir}/%{name}/version
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
%{_mandir}/man5/%{name}-netmap.5.*
%{_mandir}/man5/%{name}-params.5.*
%{_mandir}/man5/%{name}-policy.5.*
%{_mandir}/man5/%{name}-providers.5.*
%{_mandir}/man5/%{name}-proxyarp.5.*
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
%{_mandir}/man5/%{name}-arprules.5.*
%{_mandir}/man5/%{name}-blrules.5.*
%{_mandir}/man5/%{name}-conntrack.5.*
%{_mandir}/man5/%{name}-rtrules.5.*
%{_mandir}/man5/%{name}-stoppedrules.5.*
%{_mandir}/man8/%{name}.8.*
%dir %{_datadir}/%{name}/Shorewall
%{_datadir}/shorewall/Shorewall/*.pm
%{_datadir}/%{name}/compiler.pl
%{_datadir}/%{name}/prog.footer

%files -n %{name6}
%doc %{name6}-%{ipv6_ver}/{changelog.txt,releasenotes.txt,tunnel,ipsecvpn,Samples6}
%dir %{_sysconfdir}/%{name6}
%dir %{_datadir}/%{name6}
%dir %attr(755,root,root) %{_var}/lib/%{name6}
%ghost %{_var}/lib/%{name6}/*
%ghost %{_var}/lib/%{name6}/.??*
%config(noreplace) %{_sysconfdir}/%{name6}/*
%config %{_sysconfdir}/logrotate.d/%{name6}
%attr(755,root,root) /sbin/%{name6}
%{_unitdir}/shorewall6.service
%{_datadir}/%{name6}/action*
%{_datadir}/%{name6}/configpath
%{_datadir}/%{name6}/functions
%{_datadir}/%{name6}/helpers
%{_datadir}/%{name6}/lib.*
%{_datadir}/%{name6}/macro.*
%{_datadir}/%{name6}/modules*
%{_datadir}/%{name6}/version
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
%{_mandir}/man5/%{name6}-params.5.*
%{_mandir}/man5/%{name6}-policy.5.*
%{_mandir}/man5/%{name6}-providers.5.*
%{_mandir}/man5/%{name6}-routestopped.5.*
%{_mandir}/man5/%{name6}-rules.5.*
%{_mandir}/man5/%{name6}-tcclasses.5.*
%{_mandir}/man5/%{name6}-tcdevices.5.*
%{_mandir}/man5/%{name6}-tcinterfaces.5.*
%{_mandir}/man5/%{name6}-tcpri.5.*
%{_mandir}/man5/%{name6}-masq.5.*
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
%{_mandir}/man5/%{name6}-blrules.5.*
%{_mandir}/man5/%{name6}-conntrack.5.*
%{_mandir}/man5/%{name6}-rtrules.5.*
%{_mandir}/man5/%{name6}-stoppedrules.5.*
%{_mandir}/man8/%{name6}.8.*

%files core
%doc %{name}-core-%{version}/*.txt
%dir %{_datadir}/shorewall/
%{_datadir}/shorewall/coreversion
%{_datadir}/shorewall/functions
%{_datadir}/shorewall/lib.base
%{_datadir}/shorewall/lib.cli
%{_datadir}/shorewall/lib.common
%{_datadir}/shorewall/shorewallrc
%{_datadir}/%{name}/wait4ifup

%files lite
%doc %{name}-lite-%{version_lite}/*.txt
%dir %{_datadir}/%{name}-lite
%dir %attr(755,root,root) %{_var}/lib/%{name}-lite
%ghost %{_var}/lib/%{name}-lite/*
%config(noreplace) %{_sysconfdir}/%{name}-lite/*
%config %{_sysconfdir}/logrotate.d/%{name}-lite
%attr(755,root,root) /sbin/%{name}-lite
%{_unitdir}/shorewall-lite.service
%{_datadir}/%{name}-lite/configpath
%{_datadir}/%{name}-lite/functions
%{_datadir}/%{name}-lite/lib.*
%{_datadir}/%{name}-lite/modules*
%{_datadir}/%{name}-lite/shorecap
%{_datadir}/%{name}-lite/version
%{_datadir}/%{name}-lite/helpers
%{_mandir}/man5/%{name}-lite*
%{_mandir}/man8/%{name}-lite*

%files -n %{name6}-lite
%doc %{name6}-lite-%{ipv6_lite_ver}/*.txt
%dir %{_datadir}/%{name6}-lite
%dir %attr(755,root,root) %{_var}/lib/%{name6}-lite
%ghost %{_var}/lib/%{name6}-lite/*
%config(noreplace) %{_sysconfdir}/%{name6}-lite/*
%config %{_sysconfdir}/logrotate.d/%{name6}-lite
%attr(755,root,root) /sbin/%{name6}-lite
%{_unitdir}/shorewall6-lite.service
%{_datadir}/%{name6}-lite/configpath
%{_datadir}/%{name6}-lite/functions
%{_datadir}/%{name6}-lite/lib.*
%{_datadir}/%{name6}-lite/modules*
%{_datadir}/%{name6}-lite/shorecap
%{_datadir}/%{name6}-lite/version
%{_datadir}/%{name6}-lite/helpers
%{_mandir}/man5/%{name6}-lite*
%{_mandir}/man8/%{name6}-lite*

%files init
%doc shorewall-init-%{version}/*.txt
%{_sysconfdir}/NetworkManager/dispatcher.d/01-shorewall
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-init
%config %{_sysconfdir}/logrotate.d/%{name}-init
%{_datadir}/shorewall-init
%{_unitdir}/shorewall-init.service
%{_mandir}/man8/%{name}-init.8.*

%files doc
%doc %{name}-docs-html-%{version}/*


%changelog
* Mon Nov 14 2011 Oden Eriksson <oeriksson@mandriva.com> 4.4.25-1.2
- built for updates

* Tue Nov 10 2011 Antoine Ginies <aginies@mandriva.com> 4.4.25-1.1mdv2011.0
- use the 4.4.25 release to fix shorewall systemd integration on 2011 release

* Wed Nov 02 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.25-1mdv2012.0
+ Revision: 712303
- drop all systemd patches, not needed now
- update to new version 4.4.25
- enable by default shorewall service

* Tue Oct 11 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.24-4
+ Revision: 704350
- patch all *.service files to remove not recognized option ExecReload by systemd

* Tue Oct 11 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.24-2
+ Revision: 704334
- correct requires on systemd-sysvinit

* Tue Oct 11 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.24-1
+ Revision: 704304
- drop patch 0,1,2 and 3
- package shorewall-init
- chage group to System/Configuration/Networking
- change naming scheme for subpackages (shorewall-ipv6 -> shorewall6)
- add provides and obsoletes for old names
- add corresponding to packages scriplets (post,preun,postun and triggerun) for systemd
- Patch9: start service after network.target
- update to new version 4.4.24
- enable support for systemd
- enable AUTOMAKE option, this compiles rules ony when any changes occurs, should have impact on boot time

* Sat Sep 10 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.23.1-1
+ Revision: 699192
- update to new version 4.4.23.1
- use function to add comment in config files instead of a patch 4

* Tue May 03 2011 Eugeni Dodonov <eugeni@mandriva.com> 4.4.19.1-2
+ Revision: 664975
- Add requires on dash (#63183)

* Sun Apr 17 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.19.1-1
+ Revision: 654619
- update to new version 4.4.19.1
- drop patch 5
- fix file list

* Thu Feb 24 2011 Oden Eriksson <oeriksson@mandriva.com> 4.4.17-1
+ Revision: 639606
- 4.4.17
- rediff patches
- conform to rpm5 due to the removal of the %%exclude macro

* Sun Aug 29 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.12.1-1mdv2011.0
+ Revision: 574000
- update to new version 4.4.12.1
- redeiff patches 4 i 5
- remove requires on dash, no need to redundant requires

* Thu Aug 05 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.11-2mdv2011.0
+ Revision: 566063
- switch default shebang to dash (speed up is almost 1 second)
- add requires to dash

* Thu Jul 15 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 4.4.11-1mdv2011.0
+ Revision: 553762
- update to new version 4.4.11
- rediff patches 4 and 5
- fix file list

* Tue May 18 2010 Eugeni Dodonov <eugeni@mandriva.com> 4.4.9-2mdv2010.1
+ Revision: 545278
- P5: use default kernel module suffix.

* Sat May 08 2010 Eugeni Dodonov <eugeni@mandriva.com> 4.4.9-1mdv2010.1
+ Revision: 543542
- Updated to 4.4.9.

* Fri Mar 26 2010 Eugeni Dodonov <eugeni@mandriva.com> 4.4.8-1mdv2010.1
+ Revision: 527662
- Updated to 4.4.8.

* Tue Feb 23 2010 Eugeni Dodonov <eugeni@mandriva.com> 4.4.7-2mdv2010.1
+ Revision: 510406
- Updated to 4.4.7.5.

* Wed Feb 17 2010 Eugeni Dodonov <eugeni@mandriva.com> 4.4.7-1mdv2010.1
+ Revision: 507244
- Updated to 4.4.7.4.

* Mon Jan 18 2010 Eugeni Dodonov <eugeni@mandriva.com> 4.4.6-1mdv2010.1
+ Revision: 493159
- New version 4.4.6.

* Thu Dec 24 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.5-2mdv2010.1
+ Revision: 482167
- New version 4.4.5.4.

* Wed Dec 23 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.5-1mdv2010.1
+ Revision: 481680
- Updated to 4.4.5.3.
  Added logrotate files.

* Tue Nov 10 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.3-1mdv2010.1
+ Revision: 464079
- Updated to 4.4.3.

* Sun Oct 04 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.2-2mdv2010.0
+ Revision: 453691
- Updated shorewall subpackage to 4.4.2.2.
- Updated to 4.4.2.

* Fri Sep 04 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.1-1mdv2010.0
+ Revision: 431580
- Updated to 4.4.1.2.

* Tue Aug 25 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.0-3mdv2010.0
+ Revision: 421023
- Adding missing comments to delimit last lines in 4.4.0 config files (breaks
  drakfirewall sometimes).

* Sun Aug 16 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.0-2mdv2010.0
+ Revision: 417118
- Added README.urpmi regarding 4.4.0 version upgrade.

* Sun Aug 16 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.4.0-1mdv2010.0
+ Revision: 416738
- Updated to shorewall-4.4.0 final.
  Obsoleting shorewall-common, shorewall-perl and shorewall-shell,
  as they are no loger supported.

* Sun Jun 21 2009 Frederik Himpe <fhimpe@mandriva.org> 4.2.10-1mdv2010.0
+ Revision: 387591
- Update to new version 4.2.10

* Sat May 16 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.9-1mdv2010.0
+ Revision: 376307
- Updated to 4.2.9.

* Fri Apr 17 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.8-2mdv2009.1
+ Revision: 367920
- Updated shorewall-perl to 4.2.8.1 (bugfix).

* Thu Apr 16 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.8-1mdv2009.1
+ Revision: 367755
- Added 4.2.8.sha1sums.
- Updated to version 4.2.8.

* Mon Mar 09 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.6-2mdv2009.1
+ Revision: 353315
- Installing correct permissions for shorewall config files.

* Sun Feb 15 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.6-1mdv2009.1
+ Revision: 340686
- Updated to new upstream 4.2.6.

* Mon Feb 09 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.5-3mdv2009.1
+ Revision: 338872
- Updated shorewall-perl to version 5.2.5.3 and shorewall6 to version 4.2.5.1.

* Sat Jan 24 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.5-2mdv2009.1
+ Revision: 333163
- Now ipv6 version of shorewall actually installs.

* Thu Jan 22 2009 Eugeni Dodonov <eugeni@mandriva.com> 4.2.5-1mdv2009.1
+ Revision: 332620
- Update to new version 4.2.5.

* Tue Jan 20 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.2.4-2mdv2009.1
+ Revision: 331781
- update shorewall-perl to 4.2.4.6 version

* Sat Jan 03 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 4.2.4-1mdv2009.1
+ Revision: 323534
- update to new version 4.2.4
- this release introduces IPv6 support in Shoreline firewall (needs kernel-2.6.25 and iptables-1.4.1)
  o shorewall-ipv6
  o shorewall-ipv6-lite
- adapt spec file for new subpackages
- rediff both patches and add new ones for new subpackages
- shorewall-perl and shorewall-shell does not require rpm-helper

* Sun Nov 30 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.2.2-1mdv2009.1
+ Revision: 308523
- update to new version 4.2.2

* Wed Nov 05 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.2.1-1mdv2009.1
+ Revision: 300090
- update to new version 4.2.1(.1)

* Sun Oct 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.2.0-2mdv2009.1
+ Revision: 293005
- enable IPv6 support

* Sun Oct 12 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.2.0-1mdv2009.1
+ Revision: 292841
- update to new version 4.2.0

* Tue Sep 23 2008 Olivier Blin <blino@mandriva.org> 4.0.13-5mdv2009.0
+ Revision: 287298
- revert running iptables check, it should be done in iptables post instead of running this every boot

* Thu Aug 28 2008 Oden Eriksson <oeriksson@mandriva.com> 4.0.13-4mdv2009.0
+ Revision: 276811
- fix #42579 (shorewall-perl complains of missing Mult-port Match support in kernel/iptables)
- fix spec file bug in the shorewall-lite %%post script

* Mon Aug 04 2008 Frederik Himpe <fhimpe@mandriva.org> 4.0.13-3mdv2009.0
+ Revision: 263505
- New upstream version 4.0.13

* Wed Jun 18 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.0.11-3mdv2009.0
+ Revision: 225451
- update shorewall-perl to new version 4.0.11.1

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Thu May 29 2008 Gustavo De Nardin <gustavodn@mandriva.com> 4.0.11-2mdv2009.0
+ Revision: 213149
- fix missing requirement on iptables-ipv6, for Shorewall to be able to
  "handle" IPv6 (currently, DISABLE_IPV6=Yes in /etc/shorewall/shorewall.conf)

* Sun May 25 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.0.11-1mdv2009.0
+ Revision: 211074
- update to new version 4.0.11

* Tue Mar 11 2008 Olivier Blin <blino@mandriva.org> 4.0.9-3mdv2008.1
+ Revision: 185827
- do not package dirs as ghost (#38105)
- do not include . and .. in ghost files list

* Wed Feb 27 2008 Frederik Himpe <fhimpe@mandriva.org> 4.0.9-2mdv2008.1
+ Revision: 175897
- Update to bugfix release shorewall-perl-4.0.9.1

* Mon Feb 25 2008 Frederik Himpe <fhimpe@mandriva.org> 4.0.9-1mdv2008.1
+ Revision: 174942
- New upstream bugfix release

* Sat Feb 23 2008 Frederik Himpe <fhimpe@mandriva.org> 4.0.8-5mdv2008.1
+ Revision: 174093
- Add Conflicts to fix update from shorewall < 4.0 packages
  (files were moved from shorewall package to shorewall-common)

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 4.0.8-4mdv2008.1
+ Revision: 171106
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - fix ghost files one more time

* Sun Jan 27 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.0.8-2mdv2008.1
+ Revision: 158506
- fix permission of all ghost files
- add missing ghost files

* Sat Jan 26 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.0.8-1mdv2008.1
+ Revision: 158422
- update to latest release 4.0.8
- hardcode path to shorewall config files
- do not package config files twice, files in /etc/shorewall are sufficient

* Sat Jan 26 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.0.7-3mdv2008.1
+ Revision: 158257
- fix requires on iproute2
- shorewall package requires only shorewall-common and shorewall-perl, other subpackages are optional
- compile shorewal rules with perl compiler, as it is faster than shell one
- do the optimizations

* Fri Jan 25 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.0.7-2mdv2008.1
+ Revision: 158039
- add missing requires
- fix requires on subpackages
- make both initscripts mdv compiliant
- add missing scriplets
- use %%create_ghostfile
- fix permissions for initscripts and executables
- add ghost files for shorewall-lie

* Thu Jan 24 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 4.0.7-1mdv2008.1
+ Revision: 157724
- fix docs
- new version
- WARNING: big version jumps doesn't bring nothing good :)
- provide shorewall
  o common
  o lite
  o perl
  o shell
- fix file list, add %%ghost files
- better summaries and descriptions
- spec file clean
- TODO: provide patches for shorewall and shorewall-lite initscripts - cosmetics imho

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Oct 11 2007 Oden Eriksson <oeriksson@mandriva.com> 3.4.6-1mdv2008.1
+ Revision: 97137
- 3.4.6

  + Thierry Vignaud <tv@mandriva.org>
    - s/Mandrake/Mandriva/

* Sat Jun 30 2007 Olivier Blin <blino@mandriva.org> 3.4.4-2mdv2008.0
+ Revision: 46098
- fix compiler script permissions (#31651)

* Wed Jun 27 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 3.4.4-1mdv2008.0
+ Revision: 44819
- spec file clean
- new version

* Thu May 17 2007 Olivier Blin <blino@mandriva.org> 3.4.3-1mdv2008.0
+ Revision: 27675
- 3.4.3 (and package man pages)


* Tue Feb 13 2007 Olivier Blin <oblin@mandriva.com> 3.2.9-1mdv2007.0
+ Revision: 120417
- 3.2.9
- buildconflicts with apt-common so that shorewall build does not detect a Debian system
- bunzip init script

* Mon Nov 27 2006 Olivier Blin <oblin@mandriva.com> 3.2.6-1mdv2007.1
+ Revision: 87676
- 3.2.6
- Import shorewall

* Thu Aug 31 2006 Olivier Blin <blino@mandriva.com> 3.2.3-2mdv2007.0
- fix typo in changelog

* Thu Aug 31 2006 Olivier Blin <blino@mandriva.com> 3.2.3-1mdv2007.0
- 3.2.3 (this closes #24157)

* Sun Jul 23 2006 Olivier Blin <blino@mandriva.com> 3.2.1-1mdv2007.0
- 3.2.1
- drop bogons file ('nobogons' options has been eliminated in 3.0.0)

* Mon Jan 23 2006 Daouda LO <daouda@mandriva.com> 3.0.4-1mdk
- 3.0.4
- console friendly again (Tuomo Soini)

* Mon Dec 26 2005 Daouda LO <daouda@mandriva.com> 3.0.3-1mdk
- 3.0.3

* Wed Nov 30 2005 Daouda LO <daouda@mandriva.com> 3.0.2-1mdk
- 3.0.2

* Thu Nov 24 2005 Daouda LO <daouda@mandriva.com> 3.0.1-1mdk
- 3.0.1
- add Samples 
- cleanup spec
- Read The http://shorewall.net/pub/shorewall/3.0/shorewall-3.0.1/releasenotes.txt
  o Thu Nov 17 2005 Nicolas CHIPAUX <chipaux@mandriva.com> 3.0.0-1mdk
	- new version
    - cleaning spec
    - "clear" option in initscript is back
    - info about migration from 2.x to 3.x

* Fri Jul 22 2005 Daouda LO <daouda@mandrakesoft.com> 2.4.1-3mdk
- initscript priority from 25 to 10 (Michael Reinsch)
- refreshed link to firewall script (Oblin)

* Tue Jul 19 2005 Olivier Blin <oblin@mandriva.com> 2.4.1-2mdk
- enable shorewall startup

* Tue Jul 19 2005 Daouda LO <daouda@mandrakesoft.com> 2.4.1-1mdk
- Fix for security vulnerability in MACLIST processing
- Support for multiple internet interfaces to different ISPs
- Support for ipset
- updated firewall script and bogons list 
- back to shorewall genuine initscipt

* Mon Jul 11 2005 Olivier Blin <oblin@mandriva.com> 2.0.8-3mdk
- fix typo in init script to have chkconfig working again (#16657)

* Sat Apr 02 2005 Luca Berra <bluca@vodka.it> 2.0.8-2mdk
- use %%mkrel macro
- update firewall script from shorewall errata
- update bogons file from shorewall errata

* Thu Aug 26 2004 Florin <florin@mandrakesoft.com> 2.0.8-1mdk
- 2.0.8

* Thu Aug 05 2004 Florin <florin@mandrakesoft.com> 2.0.7-1mdk
- 2.0.7

* Wed Jun 30 2004 Florin <florin@mandrakesoft.com> 2.0.3a-1mdk
- 2.0.3a
- security update

* Fri Jun 25 2004 Florin <florin@mandrakesoft.com> 2.0.3-1mdk
- 2.0.3

* Sun Jun 13 2004 Florin <florin@mandrakesoft.com> 2.0.2f-1mdk
- 2.0.2f
- add the docs source
- remove the already present bogons and rf1918 files

* Thu Jun 03 2004 Florin <florin@mandrakesoft.com> 2.0.2d-1mdk
- 2.0.2d

* Tue May 18 2004 Florin <florin@mandrakesoft.com> 2.0.2a-1mdk
- 2.0.2a
- add the initdone file

* Fri May 14 2004 Florin <florin@mandrakesoft.com> 2.0.2-0.RC1.1mdk
- 2.0.2-RC1
- remove the already intergrated kernel-suffix patch

* Thu Apr 22 2004 Florin <florin@mandrakesoft.com> 2.0.1-3mdk
- add the bogons and rf1918 sources (thx to T. Backlund)

* Tue Apr 20 2004 Florin <florin@mandrakesoft.com> 2.0.1-2mdk
- add the kernel modules extension patch (bug #9311)
- the same patch fixes the Mandrake broken insmod (uses modprobe instead)

* Tue Apr 20 2004 Florin <florin@mandrakesoft.com> 2.0.1-1mdk
- 2.0.1
- samples 2.0.1
- add the netmap file

* Wed Mar 24 2004 Florin <florin@mandrakesoft.com> 2.0.0b-1mdk
- 2.0.0b

* Sat Mar 20 2004 Florin <florin@mandrakesoft.com> 2.0.0a-1mdk
- 2.0.0a
- samples 2.0.0

