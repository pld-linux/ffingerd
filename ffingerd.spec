Summary:	Secure finger daemon
Summary(pl):	Bezpieczny serwer finger
Name:		ffingerd
Version:	1.28
Release:	6
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.fu-berlin.de/pub/unix/security/ffingerd/%{name}-%{version}.tar.bz2
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-gethostbyaddr_is_in_libc_aka_no_libnsl.patch
Patch2:		%{name}-SA_LEN.patch
URL:		http://www.fefe.de/ffingerd/
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	inetdaemon
Prereq:		rc-inetd >= 0.8.1
Provides:	fingerd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	bsd-fingerd
Obsoletes:	finger-server
Obsoletes:	cfingerd
Obsoletes:	efingerd

%description
The ffingerd program is a drop-in replacement for the standard fingerd
daemon. Ffingerd is invoked by inetd and it runs as nobody. Ffingerd
does not allow global finger queries (finger @host), indirect finger
queries (finger foo@host.a@host.b), it does not give away valuable
information like the shell, login directory and time of last login,
and users can put a ".nofinger" file in their homes and then ffingerd
will respond with "That user does not want to be fingered".

%description -l pl
Program ffingerd jest zamiennikiem dla standardowego demona fingerd.
Jest uruchamiany przez inetd i pracuje jako u¿ytkownik nobody.
Ffingerd nie pozwala na zapytania globalne (finger @host), zapytania
po¶rednie (finger foo@host.a@host.b), nie wy¶wietla informacji o
pow³oce u¿ytkownika, jego katalogu domowym i czasie ostatniego
zalogowania. Umo¿liwia u¿ytkownikom stworzenie w katalogu domowym
pliku ".nofinger".

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
aclocal
%{__autoconf}
%configure \
	CFLAGS="%{rpmcflags} -D__ss_family=ss_family" \
	--enable-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/fingerd

gzip -9nf README NEWS TODO

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
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
%attr(640,root,root) /etc/sysconfig/rc-inetd/fingerd

%{_mandir}/man8/*
