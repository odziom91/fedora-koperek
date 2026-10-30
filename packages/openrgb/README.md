# OpenRGB

RPM packaging draft for [OpenRGB](https://codeberg.org/OpenRGB/OpenRGB), an open-source application for controlling RGB lighting devices.

- Version: 1.1
- Upstream: https://codeberg.org/OpenRGB/OpenRGB
- Required additional package: `hidapi-hotplug`
- Target architectures: x86_64
- Target Fedora releases: 44 and 45 (COPR build validation required)

Build `hidapi-hotplug` first. OpenRGB 1.1's Linux RPM packaging requires the matching fork.

This SPEC is an initial draft, not a verified copy of the upstream Fedora SPEC. The first COPR build must be used to confirm the correct qmake invocation, install layout, and complete `%files` list. Test USB device access and udev permissions on real hardware after installation.
