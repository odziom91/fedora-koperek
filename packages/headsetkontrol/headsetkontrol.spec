%global forgeurl https://gitlab.com/billtran1632001/headsetkontrol

Name:           headsetkontrol
Version:        2.0.4
Release:        1%{?dist}
Summary:        Kirigami interface for controlling headsets with HeadsetControl

License:        GPL-3.0-only
URL:            %{forgeurl}
Source0:        %{forgeurl}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  extra-cmake-modules

# Qt 6 modules used by the application
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtquickcontrols2-devel

# KDE Frameworks 6 and Kirigami Addons
BuildRequires:  kf6-kirigami-devel
BuildRequires:  kf6-kirigami-addons-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kcoreaddons-devel
BuildRequires:  kf6-kconfig-devel
BuildRequires:  kf6-kdbusaddons-devel
BuildRequires:  kf6-knotifications-devel
BuildRequires:  kf6-kiconthemes-devel
BuildRequires:  kf6-kstatusnotifieritem-devel
BuildRequires:  kf6-knotifyconfig-devel

# QML imports used at runtime
Requires:       kf6-kirigami
Requires:       kf6-kirigami-addons

%description
HeadsetKontrol is a graphical interface for HeadsetControl. It can monitor
headset information, show battery notifications and configure headset-specific
settings. The application is written using Qt 6, Kirigami and KDE Frameworks 6.

%prep
%autosetup -n %{name}-v%{version}

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_bindir}/headsetkontrol
%{_datadir}/applications/headsetkontrol.desktop
%{_datadir}/knotifications6/headsetkontrol.notifyrc
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/icons/hicolor/scalable/status/headsetkontrol-battery-*.svg
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%changelog
* Fri Oct 30 2026 COPR Builder <copr@example.invalid> - 2.0.4-1
- Initial COPR packaging for Fedora 45
