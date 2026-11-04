%define _version 3.15.2-b1
%define _rpmrel 1

%global _description %{expand:
DemonEditor is an Enigma2 channel and satellite list editor for
GNU/Linux. It supports editing bouquets, channels and satellites,
IPTV services, picons, receiver communication and more.
}

Name:           demon-editor
Version:        %{_version}
Release:        %{_rpmrel}%{?dist}
Summary:        Enigma2 channel and satellite list editor

License:        MIT
URL:            https://github.com/DYefremov/DemonEditor
Source0:        https://github.com/DYefremov/DemonEditor/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch

Requires:       python3
Requires:       python3-gobject
Requires:       python3-cairo
Requires:       python3-requests
Requires:       gtk3
Requires:       gtksourceview3

%description
%{_description}

%prep
%autosetup -n DemonEditor-%{version}

%build
# DemonEditor is a Python application; no compilation is required.

%install
install -dpm0755 %{buildroot}%{_datadir}/demon-editor

cp -a app extensions po start.py README.md LICENSE \
    demon-editor.desktop \
    %{buildroot}%{_datadir}/demon-editor/

# Install application launcher.
cat > %{buildroot}%{_bindir}/demon-editor <<'EOF'
#!/bin/sh
cd /usr/share/demon-editor || exit 1
exec python3 ./start.py "$@"
EOF

chmod 0755 %{buildroot}%{_bindir}/demon-editor

# Install desktop entry.
install -Dpm0644 demon-editor.desktop \
    %{buildroot}%{_datadir}/applications/demon-editor.desktop

# Configure desktop entry.
sed -i \
    -e 's|^Exec=.*|Exec=demon-editor|' \
    -e 's|^Icon=.*|Icon=/usr/share/demon-editor/app/ui/icons/hicolor/96x96/apps/demon-editor.png|' \
    %{buildroot}%{_datadir}/applications/demon-editor.desktop

%check
desktop-file-validate \
    %{buildroot}%{_datadir}/applications/demon-editor.desktop

%files
%license LICENSE
%doc README.md

%{_bindir}/demon-editor
%{_datadir}/applications/demon-editor.desktop
%{_datadir}/demon-editor/

%changelog
* Wed Nov 04 2026 OdzioM - 3.15.2-b1-1
- Initial package