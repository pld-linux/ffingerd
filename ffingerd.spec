Summary:	Secure finger daemon
Summary(pl.UTF-8):	Bezpieczny serwer finger
Name:		ffingerd
Version:	1.28
Release:	9
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.fu-berlin.de/pub/unix/security/ffingerd/%{name}-%{version}.tar.bz2
# Source0-md5:	90e2ebbe8f299e12b4c5da401c0b71b1
Source1:	%{name}.inetd
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-gethostbyaddr_is_in_libc_aka_no_libnsl.patch
Patch2:		%{name}-SA_LEN.patch
URL:		http://www.fefe.de/ffingerd/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	inetdaemon
Requires:	rc-inetd >= 0.8.1
Provides:	fingerd
Obsoletes:	bsd-fingerd
Obsoletes:	cfingerd
Obsoletes:	efingerd
Obsoletes:	finger-server
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ffingerd program is a drop-in replacement for the standard fingerd
daemon. Ffingerd is invoked by inetd and it runs as nobody. Ffingerd
does not allow global finger queries (finger @host), indirect finger
queries (finger foo@host.a@host.b), it does not give away valuable
information like the shell, login directory and time of last login,
and users can put a ".nofinger" file in their homes and then ffingerd
will respond with "That user does not want to be fingered".

%description -l pl.UTF-8
Program ffingerd jest zamiennikiem dla standardowego demona fingerd.
Jest uruchamiany przez inetd i pracuje jako użytkownik nobody.
Ffingerd nie pozwala na zapytania globalne (finger @host), zapytania
pośrednie (finger foo@host.a@host.b), nie wyświetla informacji o
powłoce użytkownika, jego katalogu domowym i czasie ostatniego
zalogowania. Umożliwia użytkownikom stworzenie w katalogu domowym
pliku ".nofinger".

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
%configure \
	CFLAGS="%{rpmcflags} -D__ss_family=ss_family" \
	--enable-ipv6
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/fingerd

%post
%service -q rc-inetd reload

%postun
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README NEWS TODO
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) /etc/sysconfig/rc-inetd/fingerd

%{_mandir}/man8/*
