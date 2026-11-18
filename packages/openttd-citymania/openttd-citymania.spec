Name:           openttd-citymania
Version:        15.3
Release:        2%{?dist}
Summary:        CityMania enhanced client for OpenTTD

License:        GPL-2.0-only AND Zlib AND MIT AND BSL-1.0 AND BSD-2-Clause AND CC0-1.0 AND Apache-2.0 AND Unicode-3.0
URL:            https://citymania.org/downloads
Source0:        https://citymania.org/static/files/client/citymania-client-%{version}-source.zip

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  unzip
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig
BuildRequires:  zlib-devel
BuildRequires:  xz-devel
BuildRequires:  lzo-devel
BuildRequires:  libzstd-devel
BuildRequires:  libpng-devel
BuildRequires:  libcurl-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libicu-devel
BuildRequires:  fluidsynth-devel
BuildRequires:  opusfile-devel
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  libglvnd-devel

# The OpenGFX package supplies the base graphics. In Fedora, it also
# depends on vanilla OpenTTD; both applications are installed side by side.
Requires:       openttd-opengfx
Requires:       hicolor-icon-theme

%description
CityMania Client is a network-compatible enhanced OpenTTD client,
providing additional interface tools, zoning overlays, railway building
features and shortcuts. It is installed alongside the Fedora OpenTTD
package under its own executable, application launcher and system data directory.
The client uses the standard OpenTTD user configuration and multiplayer
identity, including XDG configuration paths.

%prep
# The official source ZIP may contain either files at archive root or
# a single versioned top-level directory.
%autosetup -c
if [ ! -f CMakeLists.txt ]; then
    cmake_file=$(find . -mindepth 2 -maxdepth 2 -type f -name CMakeLists.txt -print -quit)
    test -n "$cmake_file"
    source_dir=${cmake_file%/CMakeLists.txt}
    find "$source_dir" -mindepth 1 -maxdepth 1 -exec mv -t . -- {} +
    rmdir "$source_dir"
fi

test -f CMakeLists.txt

%build
# Share the upstream OpenTTD user profile (XDG config/data and multiplayer identity).
# BINARY_NAME stays distinct for RPM coexistence; PERSONAL_DIR must remain .openttd.
%cmake \
    -DBINARY_NAME=%{name} \
    -DOPTION_INSTALL_FHS=ON \
    -DOPTION_PACKAGE_DEPENDENCIES=OFF \
    -DOPTION_DEDICATED=OFF \
    -DCMAKE_INSTALL_BINDIR=bin \
    -DCMAKE_INSTALL_DATADIR=share \
    -DCMAKE_INSTALL_MANDIR=share/man \
    -DCMAKE_INSTALL_DOCDIR=share/doc/%{name} \
    -DGLOBAL_DIR=%{_datadir}/%{name} \
    -DPERSONAL_DIR=.openttd
%cmake_build

%install
%cmake_install

# Distinguish this client from vanilla OpenTTD in GNOME/KDE menus.
sed -i 's/^Name=OpenTTD$/Name=OpenTTD (CityMania)/' \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# Reuse Fedora's free base graphics rather than shipping a second copy.
# The OpenGFX files reside in /usr/share/openttd/baseset/opengfx.
ln -s %{_datadir}/openttd/baseset/opengfx \
    %{buildroot}%{_datadir}/%{name}/baseset/opengfx

# The license is installed in the RPM license directory by %%license.
rm -f %{buildroot}%{_docdir}/%{name}/COPYING.md

%files
%license COPYING.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}*.xpm
%{_mandir}/man6/%{name}.6*
%{_docdir}/%{name}/

%changelog
* Wed Nov 18 2026 Fedora COPR Maintainer - 15.3-2
- Use standard OpenTTD personal directory for settings and multiplayer identity
- Keep executable, desktop entry, and system data separate from vanilla OpenTTD

* Wed Nov 18 2026 Fedora COPR - 15.3-1
- Initial RPM package for CityMania Client 15.3
- Parallel installation with vanilla OpenTTD