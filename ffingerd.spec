Summary:	secure finger daemon
Summary(pl):	bezpieczny serwer finger
Name:		ffingerd
Version:	1.23
Release:	1
Group:		Networking/Daemons
Group(pl):	Sieciowe/Demony
Copyright:	GPL
Source:		ftp://ftp.fu-berlin.de/pub/unix/security/ffingerd/%{name}-%{version}.tar.gz
Patch:		ffingerd-DESTDIR.patch
Requires:	inetd
Provides:	fingerd
#Obsoletes:	finger
BuildRoot:	/tmp/%{name}-%{version}-root

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
Jest uruchamiany przez inetd i pracuje jako u¿ytkownik nobody. 
Ffingerd nie pozwala na zapytania globalne (finger @host), zapytania 
po¶rednie (finger foo@host.a@host.b), nie wy¶wietla informacji o pow³oce
u¿ytkownika, jego katalogu domowym i czasie ostatniego zalogowania,
umo¿liwia u¿ytkownikom stworzenie w katalogu domowym pliku ".nofinger".

%prep
%setup -q
%patch -p0

%build
LDFLAGS="-s"; export LDFLAGS
%configure 
make

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT \
	install

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/* \
	README NEWS TODO

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,NEWS,TODO}.gz
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man8/*
