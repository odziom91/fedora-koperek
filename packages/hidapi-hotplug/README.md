# hidapi-hotplug

Packaging draft for the OpenRGB-maintained `hidapi-hotplug` fork.

OpenRGB 1.1's Linux RPM/DEB packages require the corresponding `hidapi-hotplug` package. Build and publish this package before building `openrgb`.

- Upstream: https://codeberg.org/OpenRGB/hidapi-hotplug
- Upstream release: `hidapi-hotplug-0.15.0`
- Target architectures: x86_64
- Target Fedora releases: 44 and 45 (COPR build validation required)

This SPEC is an initial draft and has not yet been built. Check the upstream archive's CMake options, pkg-config name, library names, and installed paths against the build log before publishing.
