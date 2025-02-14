#
# Conditional build:
%bcond_with	ffmpeg		# FFmpeg instead of GStreamer as generic media extractor
%bcond_with	gupnp		# GStreamer gupnp backend instead of discoverer
%bcond_with	icu		# ICU instead of enca for MP3 encoding detection

%define		abiver	2.0
Summary:	Tracker miners and metadata extractors
Summary(pl.UTF-8):	Narzędzia wydobywania danych dla programu Tracker
Name:		tracker-miners
Version:	2.3.5
Release:	4
# see COPYING for details
License:	LGPL v2.1+ (libs), GPL v2+ (miners)
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/tracker-miners/2.3/%{name}-%{version}.tar.xz
# Source0-md5:	0bbcab133ed33ccbf65923020f99e1cc
URL:		https://wiki.gnome.org/Projects/Tracker
BuildRequires:	dbus-devel >= 1.3.1
%{!?with_icu:BuildRequires:	enca-devel >= 1.9}
BuildRequires:	exempi-devel >= 2.1.0
# libavcodec libavformat libavutil
%{?with_ffmpeg:BuildRequires:	ffmpeg-devel >= 0.8.4}
BuildRequires:	flac-devel >= 1.2.1
BuildRequires:	gexiv2-devel
BuildRequires:	giflib-devel
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%if %{with gupnp}
BuildRequires:	gupnp-dlna-devel >= 0.9.4
BuildRequires:	gupnp-dlna-gst-devel >= 0.9.4
%endif
BuildRequires:	libcue-devel
BuildRequires:	libexif-devel >= 0.6
BuildRequires:	libgrss-devel >= 0.7
BuildRequires:	libgsf-devel >= 1.14.24
BuildRequires:	libgxps-devel
%{?with_icu:BuildRequires:	libicu-devel >= 4.8.1.1}
BuildRequires:	libiptcdata-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libosinfo-devel >= 0.2.9
BuildRequires:	libpng-devel
%ifnarch alpha ia64 m68k parisc sh4 sparc sparcv9 sparc64
BuildRequires:	libseccomp-devel >= 2.0
%endif
BuildRequires:	libtiff-devel >= 4
BuildRequires:	libvorbis-devel >= 0.22
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	meson >= 0.47
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	poppler-glib-devel >= 0.16.0
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	totem-pl-parser-devel
BuildRequires:	tracker-devel >= 2.2.0
BuildRequires:	upower-devel >= 0.9.0
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	dbus >= 1.3.1
%{!?with_icu:Requires:	enca-libs >= 1.9}
Requires:	exempi >= 2.1.0
Requires:	flac >= 1.2.1
Requires:	glib2 >= 1:2.40.0
%if %{with gupnp}
Requires:	gupnp-dlna >= 0.9.4
Requires:	gupnp-dlna-gst >= 0.9.4
%endif
Requires:	libexif >= 0.6
Requires:	libgrss >= 0.7
Requires:	libgsf >= 1.14.24
Requires:	libosinfo >= 0.2.9
Requires:	libvorbis >= 0.22
Requires:	libxml2 >= 1:2.6
Requires:	systemd-units >= 1:250.1
Requires:	tracker >= 2.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains various miners and metadata extractors for
tracker.

%description -l pl.UTF-8
Ten pakiet zawiera narzędzia wydobywania danych dla programu Tracker.

%prep
%setup -q

%build
%meson \
	--default-library=shared \
	-Dbattery_detection=upower \
	-Dcharset_detection=%{?with_icu:icu}%{!?with_icu:enca} \
	-Dfunctional_tests=false \
	-Dgeneric_media_extractor=%{?with_ffmpeg:libav}%{!?with_ffmpeg:gstreamer} \
	-Dgstreamer_backend=%{?with_gupnp:gupnp}%{!?with_gupnp:discoverer} \
	-Dsystemd_user_services=%{systemduserunitdir}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%find_lang tracker-miners

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%systemd_user_post tracker-extract.service tracker-miner-fs.service tracker-miner-rss.service tracker-writeback.service

%preun
%systemd_user_preun tracker-extract.service tracker-miner-fs.service tracker-miner-rss.service tracker-writeback.service

%postun
%glib_compile_schemas

%files -f tracker-miners.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING MAINTAINERS NEWS README.md
%attr(755,root,root) %{_libexecdir}/tracker-extract
%attr(755,root,root) %{_libexecdir}/tracker-miner-fs
%attr(755,root,root) %{_libexecdir}/tracker-miner-rss
%attr(755,root,root) %{_libexecdir}/tracker-writeback
%{systemduserunitdir}/tracker-extract.service
%{systemduserunitdir}/tracker-miner-fs.service
%{systemduserunitdir}/tracker-miner-rss.service
%{systemduserunitdir}/tracker-writeback.service
%dir %{_libdir}/%{name}-%{abiver}
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/libtracker-extract.so
%dir %{_libdir}/%{name}-%{abiver}/extract-modules
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-abw.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-bmp.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-desktop.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-dummy.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-dvi.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-epub.so
# R: flac
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-flac.so
# R: giflib
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-gif.so
# R: gstreamer gstreamer-plugins-base
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-gstreamer.so
# R: libxml2
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-html.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-icon.so
# R: libosinfo
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-iso.so
# R: libiptcdata libjpeg
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-jpeg.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-mp3.so
# R: libgsf
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-msoffice.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-msoffice-xml.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-oasis.so
# R: poppler-glib
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-pdf.so
# R: totem-plparser
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-playlist.so
# R: libpng
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-png.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-ps.so
# R: libgexiv2
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-raw.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-text.so
# R: libtiff
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-tiff.so
# R: libvorbis
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-vorbis.so
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-xmp.so
# R: libgxps
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/extract-modules/libextract-xps.so
%dir %{_libdir}/%{name}-%{abiver}/writeback-modules
# R: gstreamer gstreamer-plugins-base
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/writeback-modules/libwriteback-gstreamer.so
# R: exempi
%attr(755,root,root) %{_libdir}/%{name}-%{abiver}/writeback-modules/libwriteback-xmp.so
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Miner.Extract.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Miner.Files.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Miner.RSS.service
%{_datadir}/dbus-1/services/org.freedesktop.Tracker1.Writeback.service
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker.Extract.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker.Miner.Files.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.Tracker.Writeback.gschema.xml
%{_datadir}/glib-2.0/schemas/org.freedesktop.TrackerMiners.enums.xml
%dir %{_datadir}/tracker/miners
%{_datadir}/tracker/miners/org.freedesktop.Tracker1.Miner.Extract.service
%{_datadir}/tracker/miners/org.freedesktop.Tracker1.Miner.Files.service
%{_datadir}/tracker/miners/org.freedesktop.Tracker1.Miner.RSS.service
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/extract-rules
# standalone (builtin?) rules
%{_datadir}/%{name}/extract-rules/10-comics.rule
%{_datadir}/%{name}/extract-rules/10-ebooks.rule
%{_datadir}/%{name}/extract-rules/10-svg.rule
# modules
%{_datadir}/%{name}/extract-rules/10-abw.rule
%{_datadir}/%{name}/extract-rules/10-bmp.rule
%{_datadir}/%{name}/extract-rules/10-desktop.rule
%{_datadir}/%{name}/extract-rules/10-dvi.rule
%{_datadir}/%{name}/extract-rules/10-epub.rule
%{_datadir}/%{name}/extract-rules/10-flac.rule
%{_datadir}/%{name}/extract-rules/10-gif.rule
%{_datadir}/%{name}/extract-rules/10-html.rule
%{_datadir}/%{name}/extract-rules/10-ico.rule
%{_datadir}/%{name}/extract-rules/10-jpeg.rule
%{_datadir}/%{name}/extract-rules/10-mp3.rule
%{_datadir}/%{name}/extract-rules/10-msoffice.rule
%{_datadir}/%{name}/extract-rules/10-oasis.rule
%{_datadir}/%{name}/extract-rules/10-pdf.rule
%{_datadir}/%{name}/extract-rules/10-png.rule
%{_datadir}/%{name}/extract-rules/10-ps.rule
%{_datadir}/%{name}/extract-rules/10-raw.rule
%{_datadir}/%{name}/extract-rules/10-tiff.rule
%{_datadir}/%{name}/extract-rules/10-vorbis.rule
%{_datadir}/%{name}/extract-rules/10-xmp.rule
%{_datadir}/%{name}/extract-rules/10-xps.rule
%{_datadir}/%{name}/extract-rules/11-iso.rule
%{_datadir}/%{name}/extract-rules/11-msoffice-xml.rule
# libextract-gstreamer
%{_datadir}/%{name}/extract-rules/15-gstreamer-guess.rule
%{_datadir}/%{name}/extract-rules/15-playlist.rule
# libextract-text
%{_datadir}/%{name}/extract-rules/15-source-code.rule
# libextract-gstreamer
%{_datadir}/%{name}/extract-rules/90-gstreamer-audio-generic.rule
# libextract-gstreamer
%{_datadir}/%{name}/extract-rules/90-gstreamer-video-generic.rule
# libextract-text
%{_datadir}/%{name}/extract-rules/90-text-generic.rule
%{_mandir}/man1/tracker-extract.1*
%{_mandir}/man1/tracker-miner-fs.1*
%{_mandir}/man1/tracker-miner-rss.1*
%{_mandir}/man1/tracker-writeback.1*
