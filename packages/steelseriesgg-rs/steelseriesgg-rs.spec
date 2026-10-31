
Name:           steelseriesgg-rs
Version:        0.1.13
Release:        1%{?dist}
Summary:        Open-source SteelSeries GG replacement for Linux

License:        MIT
URL:            https://github.com/Ven0m0/steelseriesgg-rs
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  curl
BuildRequires:  gcc
BuildRequires:  systemd-rpm-macros

Requires:       systemd
Requires:       systemd-udev

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

cargo build --release --locked --bin ssgg

%install
install -Dpm0755 target/release/ssgg \
    %{buildroot}%{_bindir}/ssgg

install -Dpm0644 assets/ssgg.service \
    %{buildroot}%{_userunitdir}/ssgg.service

install -Dpm0644 assets/70-steelseries.rules \
    %{buildroot}%{_udevrulesdir}/70-steelseries.rules

%files
%license LICENSE
%doc README.md
%{_bindir}/ssgg
%{_userunitdir}/ssgg.service
%{_udevrulesdir}/70-steelseries.rules

%changelog
* Sat Oct 31 2026 OdzioM - 0.1.13-1
- Initial package
