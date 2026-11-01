%define _version 0.15.0
%define _rpmrel 2

%global _description %{expand:
OpenRGB-maintained HIDAPI fork with device hotplug support.
}

Name:           hidapi-hotplug
Version:        %{_version}
Release:        %{_rpmrel}%{?dist}
Summary:        HIDAPI fork with hotplug support for OpenRGB
License:        GPL-3.0-only OR BSD-3-Clause
URL:            https://codeberg.org/OpenRGB/hidapi-hotplug
Source0:        https://codeberg.org/OpenRGB/hidapi-hotplug/archive/hidapi-hotplug-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  libusb1-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  systemd-devel

%description %_description

%prep
%autosetup -n hidapi-hotplug

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE*
%doc README*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/hidapi-hotplug/*.cmake
%{_includedir}/hidapi-hotplug/

%changelog
* Sat Oct 31 2026 fedora-koperek maintainer <noreply@example.invalid> - 0.15.0-1
- Initial packaging draft for OpenRGB 1.1 dependency
