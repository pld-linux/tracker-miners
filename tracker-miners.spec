%define		ver	2.0
Summary:	Tracker miners and metadata extractors
Summary(pl.UTF-8):	Narzędzia wydobywania danych dla programu Tracker
Name:		tracker-miners
Version:	2.1.5
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/tracker-miners/2.1/%{name}-%{version}.tar.xz
# Source0-md5:	92e975487af4849379d0168fa23fe9c1
URL:		https://wiki.gnome.org/Projects/Tracker
BuildRequires:	intltool >= 0.40.0
BuildRequires:	pkgconfig
BuildRequires:	tracker-devel >= 2.0
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains various miners and metadata extractors for
tracker.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia wydobywania danych dla programu Tracker.

%prep
%setup -q

%build
%configure \
	--enable-libvorbis \
	--enable-libflac \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{ver}/*.a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{ver}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{ver}/extract-modules/*.a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{ver}/extract-modules/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{ver}/writeback-modules/*.a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{ver}/writeback-modules/*.la

%find_lang tracker-miners

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f tracker-miners.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS
%{_sysconfdir}/xdg/autostart/tracker-*.desktop
%{systemduserunitdir}/tracker-*.service
%attr(755,root,root) %{_libdir}/%{name}-%{ver}/libtracker-extract.so.0.0.0
%attr(755,root,root) %{_libdir}/%{name}-%{ver}/libtracker-extract.so.0
%attr(755,root,root) %{_libdir}/%{name}-%{ver}/libtracker-extract.so
%dir %{_libdir}/%{name}-%{ver}
%dir %{_libdir}/%{name}-%{ver}/extract-modules
%dir %{_libdir}/%{name}-%{ver}/writeback-modules
%attr(755,root,root) %{_libdir}/tracker-miners-2.0/extract-modules/libextract-*.so
%attr(755,root,root) %{_libdir}/tracker-miners-2.0/writeback-modules/libwriteback-*.so
%attr(755,root,root) %{_prefix}/libexec/tracker-*
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Miner.Applications.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Miner.Extract.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Miner.Files.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Miner.RSS.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Writeback.service
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker.Extract.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker.Miner.Files.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker.Writeback.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.TrackerMiners.enums.xml
%{_mandir}/man1/tracker-extract.1*
%{_mandir}/man1/tracker-miner-fs.1*
%{_mandir}/man1/tracker-miner-rss.1*
%{_mandir}/man1/tracker-writeback.1*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/extract-rules
%dir %{_datadir}/tracker-tests
%{_datadir}/tracker-miners/extract-rules/*.rule
%{_datadir}/tracker-tests/01-writeback.py
%dir %{_datadir}/tracker/miners
%{_datadir}/tracker/miners/org.freedesktop.Tracker1.Miner.Applications.service
%{_datadir}/tracker/miners/org.freedesktop.Tracker1.Miner.Extract.service
%{_datadir}/tracker/miners/org.freedesktop.Tracker1.Miner.Files.service
%{_datadir}/tracker/miners/org.freedesktop.Tracker1.Miner.RSS.service

