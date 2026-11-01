# This .spec file is based on:
# Arctis Sound Manager
# Author: loteran <https://github.com/loteran/>
# Project: https://github.com/loteran/Arctis-Sound-Manager

Name:           arctis-sound-manager
Version:        1.7.1
Release:        1%{?dist}
Summary:        SteelSeries Arctis headset manager for Linux

License:        GPL-3.0-or-later
URL:            https://github.com/loteran/Arctis-Sound-Manager
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildArch:      noarch

# Python packaging
BuildRequires:  python3-devel
BuildRequires:  python3-installer
BuildRequires:  python3-ruamel-yaml
BuildRequires:  uv
BuildRequires:  python3-uv-build

# RPM integration
BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

# The upstream wheel metadata has requirements newer than some Fedora
# packages. Use Fedora's system dependencies declared explicitly below.
%global __requires_exclude python3[0-9.]*dist\\((ruamel-yaml|pyudev)\\)

# Runtime Python dependencies
Requires:       python3-babel
Requires:       python3-dbus-next
Requires:       python3-pillow
Requires:       python3-pulsectl
Requires:       python3-pyside6
Requires:       python3-pyudev
Requires:       python3-pyusb
Requires:       python3-ruamel-yaml

# Audio stack
Requires:       pipewire
Requires:       pipewire-pulseaudio
Requires:       wireplumber
Requires:       pulseaudio-libs
Requires:       pulseaudio-utils
Requires:       libusb1

# Runtime tools and plugins
Requires:       curl
Requires:       ladspa-swh-plugins

# Optional dependencies for the Clips feature.
# Clips is disabled by default.
Recommends:     python3-gobject
Recommends:     pipewire-gstreamer
Recommends:     gstreamer1-plugins-base
Recommends:     gstreamer1-plugins-good
Recommends:     gstreamer1-plugins-bad-free
Recommends:     gstreamer1-plugins-ugly-free
Recommends:     ffmpeg-free

%description
Arctis Sound Manager is a Linux application for configuring SteelSeries
Arctis headsets. It provides headset device management, a multi-channel
audio mixer, Sonar-style parametric equalizer, virtual surround sound,
ChatMix, microphone processing and PipeWire integration.

%prep
%autosetup -n Arctis-Sound-Manager-%{version}

%build
# Use Fedora's system Python and the system-installed uv_build backend.
# Do not create an isolated build environment or download Python packages.
export UV_PYTHON_DOWNLOADS=never
export UV_SYSTEM_PYTHON=1

uv build \
    --wheel \
    --no-build-isolation \
    --python /usr/bin/python3

%install
# Install the wheel produced during %build.
python3 -m installer --destdir=%{buildroot} dist/*.whl

# Generate udev rules from the upstream device definitions.
install -d %{buildroot}%{_udevrulesdir}

python3 scripts/generate_udev_rules.py \
    src/arctis_sound_manager/devices/ \
    > %{buildroot}%{_udevrulesdir}/91-steelseries-arctis.rules

python3 scripts/generate_udev_rules.py --uaccess \
    src/arctis_sound_manager/devices/ \
    > %{buildroot}%{_udevrulesdir}/70-steelseries-arctis-uaccess.rules

# Systemd user services.
install -Dpm0644 systemd/arctis-manager.service \
    %{buildroot}%{_userunitdir}/arctis-manager.service

install -Dpm0644 systemd/arctis-video-router.service \
    %{buildroot}%{_userunitdir}/arctis-video-router.service

install -Dpm0644 systemd/arctis-stream-guard.service \
    %{buildroot}%{_userunitdir}/arctis-stream-guard.service

install -Dpm0644 systemd/app-ArctisManager.service \
    %{buildroot}%{_userunitdir}/app-ArctisManager.service

# Dinit service templates.
install -Dpm0644 dinit/arctis-manager \
    %{buildroot}%{_datadir}/%{name}/dinit/arctis-manager

install -Dpm0644 dinit/arctis-video-router \
    %{buildroot}%{_datadir}/%{name}/dinit/arctis-video-router

install -Dpm0644 dinit/arctis-stream-guard \
    %{buildroot}%{_datadir}/%{name}/dinit/arctis-stream-guard

install -Dpm0644 dinit/arctis-gui \
    %{buildroot}%{_datadir}/%{name}/dinit/arctis-gui

install -Dpm0644 dinit/pipewire-filter-chain \
    %{buildroot}%{_datadir}/%{name}/dinit/pipewire-filter-chain

install -Dpm0755 scripts/asm-diag-dinit.py \
    %{buildroot}%{_bindir}/asm-diag-dinit

# Helper used when restarting user services after an upgrade.
install -Dpm0755 scripts/restart-user-services.sh \
    %{buildroot}%{_prefix}/lib/%{name}/restart-user-services.sh

# AppStream catalog.
install -d %{buildroot}%{_datadir}/swcatalog/xml

python3 scripts/generate_appstream_catalog.py \
    --output %{buildroot}%{_datadir}/swcatalog/xml/%{name}.xml.gz

chmod 0644 %{buildroot}%{_datadir}/swcatalog/xml/%{name}.xml.gz

# Desktop entry.
install -Dpm0644 \
    src/arctis_sound_manager/desktop/ArctisManager.desktop \
    %{buildroot}%{_datadir}/applications/ArctisManager.desktop

desktop-file-validate \
    %{buildroot}%{_datadir}/applications/ArctisManager.desktop

# Application icon.
install -Dpm0644 \
    src/arctis_sound_manager/gui/images/steelseries_logo.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/arctis-manager.svg

# KDE Plasma widget.
PLASMOID_DIR=%{buildroot}%{_datadir}/plasma/plasmoids/com.github.loteran.arctis-sound-manager

install -Dpm0644 \
    src/arctis_sound_manager/desktop/plasmoid/metadata.json \
    "$PLASMOID_DIR/metadata.json"

python3 scripts/generate_plasmoid_i18n.py

for f in main.qml plasma5.qml tr.js strings.js; do
    install -Dpm0644 \
        "src/arctis_sound_manager/desktop/plasmoid/contents/ui/$f" \
        "$PLASMOID_DIR/contents/ui/$f"
done

# GNOME Shell extension.
GNOME_EXT=asm-chatmix-osd@loteran.github.com

for f in metadata.json extension.js; do
    install -Dpm0644 \
        "src/arctis_sound_manager/desktop/gnome-shell/$GNOME_EXT/$f" \
        "%{buildroot}%{_datadir}/gnome-shell/extensions/$GNOME_EXT/$f"
done

# AppStream metainfo.
python3 scripts/generate_metainfo_releases.py --in-place

install -Dpm0644 \
    src/arctis_sound_manager/desktop/com.github.loteran.arctis-sound-manager.metainfo.xml \
    %{buildroot}%{_metainfodir}/com.github.loteran.arctis-sound-manager.metainfo.xml

appstream-util validate-relax --nonet \
    %{buildroot}%{_metainfodir}/com.github.loteran.arctis-sound-manager.metainfo.xml

# PipeWire configuration templates.
install -Dpm0644 \
    scripts/pipewire/10-arctis-virtual-sinks.conf \
    %{buildroot}%{_datadir}/%{name}/pipewire/10-arctis-virtual-sinks.conf

install -Dpm0644 \
    scripts/pipewire/sink-virtual-surround-7.1-hesuvi.conf \
    %{buildroot}%{_datadir}/%{name}/pipewire/sink-virtual-surround-7.1-hesuvi.conf

# Filter-chain service template.
install -Dpm0644 scripts/filter-chain.service \
    %{buildroot}%{_datadir}/%{name}/filter-chain.service

# Headset device definitions.
install -d %{buildroot}%{_datadir}/%{name}/devices

install -m0644 src/arctis_sound_manager/devices/*.yaml \
    %{buildroot}%{_datadir}/%{name}/devices/

# First-run desktop autostart.
install -Dpm0644 debian/asm-first-run.desktop \
    %{buildroot}/etc/xdg/autostart/asm-first-run.desktop

%post
%systemd_user_post arctis-manager.service arctis-video-router.service arctis-stream-guard.service app-ArctisManager.service

# Reload udev rules. Do not trigger USB devices during package installation.
udevadm control --reload-rules || :

%preun
%systemd_user_preun arctis-manager.service arctis-video-router.service arctis-stream-guard.service app-ArctisManager.service

%postun
%systemd_user_postun arctis-manager.service arctis-video-router.service arctis-stream-guard.service app-ArctisManager.service

%files
%license LICENSE
%doc README.md CHANGELOG.md

# Python application.
%{python3_sitelib}/arctis_sound_manager/
%{python3_sitelib}/arctis_sound_manager-*.dist-info/

# Command-line applications.
%{_bindir}/asm-daemon
%{_bindir}/asm-gui
%{_bindir}/asm-cli
%{_bindir}/asm-router
%{_bindir}/asm-stream-guard
%{_bindir}/asm-clipd
%{_bindir}/asm-setup
%{_bindir}/asm-diag-dinit

# udev rules.
%{_udevrulesdir}/91-steelseries-arctis.rules
%{_udevrulesdir}/70-steelseries-arctis-uaccess.rules

# Systemd user services.
%{_userunitdir}/arctis-manager.service
%{_userunitdir}/arctis-video-router.service
%{_userunitdir}/arctis-stream-guard.service
%{_userunitdir}/app-ArctisManager.service

# Dinit templates and helper.
%{_datadir}/%{name}/dinit/
%{_prefix}/lib/%{name}/restart-user-services.sh

# AppStream and desktop integration.
%{_datadir}/swcatalog/xml/%{name}.xml.gz
%{_datadir}/applications/ArctisManager.desktop
%{_datadir}/icons/hicolor/scalable/apps/arctis-manager.svg
%{_metainfodir}/com.github.loteran.arctis-sound-manager.metainfo.xml

# KDE Plasma widget.
%{_datadir}/plasma/plasmoids/com.github.loteran.arctis-sound-manager/

# GNOME Shell extension.
%{_datadir}/gnome-shell/extensions/asm-chatmix-osd@loteran.github.com/

# PipeWire configuration and device definitions.
%{_datadir}/%{name}/pipewire/
%{_datadir}/%{name}/filter-chain.service
%{_datadir}/%{name}/devices/

/etc/xdg/autostart/asm-first-run.desktop

%changelog
* Sat Oct 31 2026 Fedora Koperek - 1.7.0-1
- Initial Fedora Koperek packaging
