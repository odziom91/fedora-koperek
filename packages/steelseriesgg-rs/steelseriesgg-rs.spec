%define _version 0.1.13
%define _rpmrel 3

Name:           steelseriesgg-rs
Version:        %{_version}
Release:        %{_rpmrel}%{?dist}
Summary:        Open-source SteelSeries GG replacement for Linux

License:        MIT
URL:            https://github.com/Ven0m0/steelseriesgg-rs
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  systemd-rpm-macros

# GUI
BuildRequires: gtk3-devel
BuildRequires: webkit2gtk4.1-devel

# feature - Audio
# BuildRequires: pulseaudio-libs-devel

Requires:       systemd
Requires:       systemd-udev
Requires:       gtk3
Requires:       webkit2gtk4.1

# feature audio support
# Requires:       pulseaudio-libs

%description
Open-source SteelSeries GG replacement for Linux.
Provides RGB lighting, device control, profiles and
a GameSense-compatible server.

%prep
%autosetup -n steelseriesgg-rs-%{version}

%build
export RUSTUP_HOME="%{_builddir}/rustup"
export CARGO_HOME="%{_builddir}/cargo"

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
    | sh -s -- -y --profile minimal --default-toolchain stable

export PATH="$CARGO_HOME/bin:$PATH"

rustc --version
cargo --version

cargo build --release --locked --features "desktop sonar" --bin ssgg --bin ssgg-gui

%install
install -Dpm0755 target/release/ssgg \
    %{buildroot}%{_bindir}/ssgg

install -Dpm0755 target/release/ssgg-gui \
    %{buildroot}%{_bindir}/ssgg-gui

install -Dpm0644 assets/ssgg-gui.desktop \
    %{buildroot}%{_datadir}/applications/ssgg-gui.desktop

install -Dpm0644 assets/ssgg.service \
    %{buildroot}%{_userunitdir}/ssgg.service

install -Dpm0644 assets/70-steelseries.rules \
    %{buildroot}%{_udevrulesdir}/70-steelseries.rules

%files
%license LICENSE
%doc README.md
%{_bindir}/ssgg
%{_bindir}/ssgg-gui
%{_datadir}/applications/ssgg-gui.desktop
%{_userunitdir}/ssgg.service
%{_udevrulesdir}/70-steelseries.rules

%changelog
* Sat Oct 31 2026 OdzioM - 0.1.13-2
- Initial package
