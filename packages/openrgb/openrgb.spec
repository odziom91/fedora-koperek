# This .spec file is based on:
# OpenRGB
# Project: https://gitlab.com/CalcProgrammer1/OpenRGB

%global _description %{expand:
OpenRGB is an open-source application for controlling RGB lighting devices
from different manufacturers.
}
%global debug_package %{nil}

Name:           openrgb
Version:        1.1
Release:        1%{?dist}
Summary:        Open source RGB lighting control
License:        GPL-2.0-only AND GPL-3.0-or-later
URL:            https://codeberg.org/OpenRGB/OpenRGB
Source0:        https://codeberg.org/OpenRGB/OpenRGB/archive/release_%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  libcurl-devel
BuildRequires:  libusb1-devel
BuildRequires:  make
BuildRequires:  mbedtls-devel
BuildRequires:  pkgconfig
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  hidapi-hotplug

Requires:       hidapi-hotplug

%description %_description

%prep
%setup -q -c -T
%{__tar} -xzf %{SOURCE0} --strip-components=1
sed -i 's|^Exec=openrgb$|Exec=env QT_STYLE_OVERRIDE=Fusion openrgb|' qt/org.openrgb.OpenRGB.desktop

%build
# OpenRGB uses qmake. The HID hotplug feature must be enabled and linked
# against the OpenRGB hidapi-hotplug fork.
qmake6 OpenRGB.pro HID_HOTPLUG_ENABLED=1
%make_build

%install
# Upstream's packaging helper generates the install payload. This draft uses
# the project's standard install target; adjust after checking the build log.
%make_install INSTALL_ROOT=%{buildroot} PREFIX=%{_prefix}

%files
%license LICENSE*
%doc README*
%{_bindir}/openrgb
%{_datadir}/applications/org.openrgb.OpenRGB.desktop
%{_datadir}/icons/hicolor/128x128/apps/org.openrgb.OpenRGB.png
%{_datadir}/metainfo/org.openrgb.OpenRGB.metainfo.xml
%{_prefix}/lib/systemd/system/openrgb.service
%{_prefix}/lib/tmpfiles.d/openrgb.conf

%changelog
* Sat Oct 31 2026 fedora-koperek maintainer <noreply@example.invalid> - 1.1-1
- Initial packaging draft for OpenRGB 1.1
