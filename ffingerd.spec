Summary:	Secure finger daemon
Summary(pl):	Bezpieczny serwer finger
Name:		ffingerd
Version:	1.25
Release:	4
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
License:	GPL
Source:		ftp://ftp.fu-berlin.de/pub/unix/security/ffingerd/%{name}-%{version}.tar.bz2
Source1:	%{name}.inetd
Patch0:		ffingerd-DESTDIR.patch
Patch1:		http://www.misiek.eu.org/ipv6/ffingerd-1.25.ipv6.patch.gz
Requires:	inetdaemon
Prereq:		rc-inetd >= 0.8.1
Provides:	fingerd
BuildRoot:	/tmp/%{name}-%{version}-root
Obsoletes:	bsd-fingerd
Obsoletes:	finger-server
Obsoletes:	cfingerd

%description
The ffingerd program is a drop-in replacement for the standard fingerd
daemon. Ffingerd is invoked by inetd and it runs as nobody. Ffingerd does
not allow global finger queries (finger @host), indirect finger queries
(finger foo@host.a@host.b), it does not give away valuable information like
 the shell, login directory and time of last login, and users can put a
".nofinger" file in their homes and then ffingerd will respond with "That
user does not want to be fingered".

%description -l pl
Program ffingerd jest zamiennikiem dla standardowego demona fingerd. Jest
uruchamiany przez inetd i pracuje jako użytkownik nobody. Ffingerd nie
pozwala na zapytania globalne (finger @host), zapytania  pośrednie (finger
foo@host.a@host.b), nie wyświetla informacji o powłoce użytkownika, jego
katalogu domowym i czasie ostatniego zalogowania. Umożliwia użytkownikom
stworzenie w katalogu domowym pliku ".nofinger".

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
LDFLAGS="-s"; export LDFLAGS
autoconf
%configure --enable-ipv6
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ffingerd

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/* \
	README NEWS TODO

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS,TODO}.gz
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/ffingerd

%{_mandir}/man8/*
