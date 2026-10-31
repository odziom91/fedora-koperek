%global _description %{expand:
OpenRGB is an open-source application for controlling RGB lighting devices
from different manufacturers.
}

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

%build
# OpenRGB uses qmake. The HID hotplug feature must be enabled and linked
# against the OpenRGB hidapi-hotplug fork.
%qmake6 OpenRGB.pro HID_HOTPLUG_ENABLED=1
%make_build

%install
# Upstream's packaging helper generates the install payload. This draft uses
# the project's standard install target; adjust after checking the build log.
%make_install

%files
%license LICENSE*
%doc README*
%{_bindir}/openrgb
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/openrgb/
%{_udevrulesdir}/*openrgb*.rules

%changelog
* Sat Oct 31 2026 fedora-koperek maintainer <noreply@example.invalid> - 1.1-1
- Initial packaging draft for OpenRGB 1.1
