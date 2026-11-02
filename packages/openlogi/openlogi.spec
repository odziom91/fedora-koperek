# Fedora COPR spec for the OpenLogi Linux Tray fork.
# Source0 is a RELEASE ASSET containing git-tagged sources + vendored Cargo
# dependencies + gpui-component theme files (prepared by prepare-openlogi-source.sh).
# It is NOT GitHub's automatically generated "Source code" archive.

Name:           openlogi
Version:        0.8.20
Release:        1%{?dist}
Summary:        Logitech device settings with a Linux status notifier tray
License:        MIT AND Apache-2.0 AND 0BSD AND BSD-2-Clause AND BSD-3-Clause AND ISC AND Unicode-3.0 AND Zlib AND CC0-1.0 AND MPL-2.0 AND Unlicense AND bzip2-1.0.6 AND CDLA-Permissive-2.0
URL:            https://github.com/Pioterr665/OpenLogiTray

%global linuxtray_tag v%{version}-linuxtray
%global source_archive openlogi-%{version}-linuxtray-vendored.tar.gz
Source0:        https://github.com/Pioterr665/OpenLogiTray/releases/download/%{linuxtray_tag}/%{source_archive}

BuildRequires:  rust >= 1.99
BuildRequires:  cargo >= 1.99
BuildRequires:  gcc-c++
BuildRequires:  clang-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  kernel-headers
BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  dbus-daemon
Requires:       dbus

%description
Local Logitech HID++ device configuration and button remapping with a
session-bus StatusNotifierItem tray for KDE Plasma and GNOME when an
AppIndicator/StatusNotifierItem extension is installed.

%prep
# Our generated tarball has a predictable openlogi-X.Y.Z/ root directory.
%autosetup -p1

test -f Cargo.lock
test -d vendor
test -s .cargo/config.toml
test -f upstream-themes/catppuccin.json

%build
export CARGO_HOME="$PWD/.cargo-home"
export CARGO_NET_OFFLINE=true
export CARGO_INCREMENTAL=0
export OPENLOGI_THEMES_DIR="$PWD/upstream-themes"
cargo build --release --frozen \
    -p openlogi -p openlogi-desktop -p openlogi-agent -p openlogi-overlay \
    --bin openlogi --bin openlogi-desktop \
    --bin openlogi-agent --bin openlogi-overlay

%install
for binary in openlogi openlogi-desktop openlogi-agent openlogi-overlay; do
    install -Dpm0755 target/release/$binary %{buildroot}%{_bindir}/$binary
done
install -Dpm0644 packaging/linux/desktop/openlogi.desktop \
    %{buildroot}%{_datadir}/applications/openlogi.desktop
install -Dpm0644 packaging/linux/systemd/openlogi-agent.service \
    %{buildroot}%{_userunitdir}/openlogi-agent.service
install -Dpm0644 packaging/linux/udev/70-openlogi.rules \
    %{buildroot}%{_udevrulesdir}/70-openlogi.rules

# Upstream graphical assets have separate redistribution restrictions.
# This changes only the desktop launcher icon; audit embedded binary assets
# before publishing a public fork package.
sed -i 's/^Icon=.*/Icon=input-mouse/' \
    %{buildroot}%{_datadir}/applications/openlogi.desktop

%check
export CARGO_HOME="$PWD/.cargo-home"
export CARGO_NET_OFFLINE=true
export OPENLOGI_THEMES_DIR="$PWD/upstream-themes"
cargo test --frozen -p openlogi-agent --bin openlogi-agent tray_linux::tests
dbus-run-session -- cargo test --frozen -p openlogi-ipc private_bus_lifecycle -- --ignored
desktop-file-validate %{buildroot}%{_datadir}/applications/openlogi.desktop

%post
%systemd_user_post openlogi-agent.service
if command -v udevadm >/dev/null 2>&1; then
    udevadm control --reload-rules >/dev/null 2>&1 || :
fi

%preun
%systemd_user_preun openlogi-agent.service

%postun
%systemd_user_postun_with_restart openlogi-agent.service
if command -v udevadm >/dev/null 2>&1; then
    udevadm control --reload-rules >/dev/null 2>&1 || :
fi

%files
%license LICENSE-MIT LICENSE-APACHE
%doc README.md
%{_bindir}/openlogi
%{_bindir}/openlogi-desktop
%{_bindir}/openlogi-agent
%{_bindir}/openlogi-overlay
%{_datadir}/applications/openlogi.desktop
%{_userunitdir}/openlogi-agent.service
%{_udevrulesdir}/70-openlogi.rules

%changelog
* Mon Nov 02 2026 OpenLogiTray contributors - 0.8.20-1
- Initial Fedora build with Linux system tray support
- Add Linux system tray support
- Bundle vendored Rust dependencies for offline builds