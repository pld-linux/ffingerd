Summary:	secure finger daemon
Summary(pl):	bezpieczny serwer finger
Name:		ffingerd
Version:	1.21
Release:	1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Demony
Copyright:	GPL
Source:		ftp://ftp.fu-berlin.de/pub/unix/security/ffingerd/%{name}-%{version}.tar.gz
BuildPrereq:	autoconf >= 2.13-8
Requires:	inetd
Provides:	fingerd
Obsoletes:	finger
BuildRoot:   	/tmp/%{name}-%{version}-root

%description
The ffingerd program is a drop-in replacement for the standard fingerd
daemon. Ffingerd is invoked by inetd and it runs as nobody. Ffingerd does 
not allow global finger queries (finger @host), indirect finger queries 
(finger foo@host.a@host.b), it does not give away valuable information like 
the shell, login directory and time of last login, and users can put 
a ".nofinger" file in  their homes and then ffingerd will respond with 
"That user does not want to be fingered".

%description -l pl
Program ffingerd jest zamiennikiem dla standardowego demona fingered.
Jest uruchamiany przez inetd i pracuje jako użytkownik nobody. 
Ffingerd nie pozwala na zapytania globalne (finger @host), zapytania 
pośrednie (finger foo@host.a@host.b), nie wyświetla informacji o powłoce
użytkownika, jego katalogu domowym i czasie ostatniego zalogowania,
umożliwia użytkownikom stworzenie w katalogu domowym pliku ".nofinger".

%prep
%setup -q

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure \
	--target=%{_target_patform} \
	--host=%{_host} \
	--prefix=/usr \
	--exec_prefix=/usr
make

%install
rm -rf $RPM_BUILD_ROOT

make exec_prefix=$RPM_BUILD_ROOT/usr \
	prefix=$RPM_BUILD_ROOT/usr install

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/* \
	README NEWS TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS,TODO}.gz
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man8/*

%changelog
* Thu May 13 1999 Piotr Czerwiński <pius@pld.org.pl>
  [1.21-1]
- initial rpm release.
