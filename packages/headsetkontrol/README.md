# HeadsetKontrol – RPM / COPR packaging

This repository contains the RPM spec file and release-update helper for
[HeadsetKontrol](https://gitlab.com/billtran1632001/headsetkontrol).

## Current packaging target

- Fedora: 45 (`fedora-45-x86_64`; optionally `fedora-45-aarch64`)
- RPM name: `headsetkontrol`
- Upstream source: GitLab project `billtran1632001/headsetkontrol`
- Release policy: stable upstream Git tags only
- Initial upstream version: `v2.0.4`

The upstream README documents Fedora build dependencies. The spec also includes
the Qt 6 development packages required by the upstream CMakeLists.txt.

## Build locally on Fedora

Install the build tools and dependencies:

```bash
sudo dnf install rpm-build rpmdevtools mock \
  cmake gcc-c++ extra-cmake-modules \
  qt6-qtbase-devel qt6-qtdeclarative-devel qt6-qtquickcontrols2-devel \
  kf6-kirigami-devel kf6-kirigami-addons-devel \
  kf6-ki18n-devel kf6-kcoreaddons-devel kf6-kconfig-devel \
  kf6-kdbusaddons-devel kf6-knotifications-devel \
  kf6-kiconthemes-devel kf6-kstatusnotifieritem-devel \
  kf6-knotifyconfig-devel
```

Build the SRPM and binary RPM:

```bash
spectool -g -R headsetkontrol.spec
rpmbuild -bs headsetkontrol.spec
```

For a full isolated build, configure `mock` for Fedora 45 and use the generated
SRPM, for example:

```bash
mock -r fedora-45-x86_64 --rebuild ~/rpmbuild/SRPMS/headsetkontrol-*.src.rpm
```

The Fedora 45 chroot name should be checked against the installed Mock config
package on the build host.

## Create the COPR project

1. Sign in to https://copr.fedorainfracloud.org/.
2. Create a project named `headsetkontrol`.
3. In the project's build settings, add Fedora 45 x86_64. Add aarch64 only if
   you want to publish and test that architecture too.
4. Add a new build using **SCM** as the source type.
5. Select GitLab / Git repository as appropriate and enter the URL of this
   packaging repository (not the upstream application repository).
6. Set the branch to `main` (or your packaging branch), the spec file to
   `headsetkontrol.spec`, and the subdirectory to the repository root.
7. Start a test build. Check the build log and install the resulting RPM in a
   Fedora 45 test VM before enabling the repository for general use.

The COPR project name and owner are yours to choose. The install command below
uses `YOUR_COPR_LOGIN` as a placeholder.

## Publishing a new upstream stable release

COPR SCM builds build the packaging repository; a new tag in the upstream
application repository does not, by itself, guarantee that COPR will rebuild
this packaging repository.

When upstream publishes a new stable tag (for example `v2.0.5`):

1. Update the `Version:` field in `headsetkontrol.spec` to `2.0.5`.
2. Run `./update-version.sh v2.0.5` (this updates the spec field).
3. Review the diff and commit/push the packaging repository.
4. Trigger a new COPR SCM build, or configure a GitLab webhook / external
   automation to trigger one after the packaging commit.

Do not package arbitrary commits from `main`; only use upstream release tags.
The helper deliberately requires an explicit tag/version so that a release is
a conscious packaging change.

## Installing from COPR

After the first successful build:

```bash
sudo dnf copr enable YOUR_COPR_LOGIN/headsetkontrol
sudo dnf install headsetkontrol
```

## HeadsetControl dependency

HeadsetKontrol is a GUI for the separate HeadsetControl utility. The upstream
project describes this relationship, but its README does not define a Fedora
package dependency or a stable package name. For that reason this spec does
**not** add a hard RPM dependency on `headsetcontrol`. Install HeadsetControl
separately using a trusted package source if you want the application to
communicate with supported headsets.

## Validation still required

This is a packaging starter based on the upstream `v2.0.4` tag, README and
CMake install rules. It has not yet been built in a Fedora 45 COPR chroot.
The first COPR build must verify the exact file list and runtime QML imports.
In particular, if the build log reports a different install path for the
notification file, icons or translations, adjust the `%files` section to match
the actual buildroot contents.
