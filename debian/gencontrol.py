#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Eugenio "g7" Paolantonio <me@medesimo.eu>
# Copyright (C) 2025 Bardia Moshiri <bardia@furilabs.com>

# TODO: Maybe use python-debian?

# Common packages for every api level
COMMON_PACKAGES = [
	"furios-quirks-writable-image",
	"android-base-passwd",
	"android-base-files",
	"udev",
	"lxc-android",
	"libhybris",
	"libhybris-utils",
	"libhybris-vulkan",
	"hadess-sensorfw-proxy",
	"furios-quirks-hybris-gl",
	"furios-quirks-qt-force-gles",
	"furios-quirks-tls-padding",
	"furios-quirks-xtables-legacy",
	"furios-quirks-vulkan",
	"gstreamer1.0-droid",
	"package-sideload",
	"flash-bootimage",
	"furios-quirks-device",
	"flashlightd",
	"flatpak-hybris",
	"flatpak-extension-gl-hybris",
	"flatpak-extension-gl-hybris-tls-padding",
	"flatpak-extension-gl-hybris-furios-workarounds",
	"gstreamer1.0-pwcompat",
	"flatpak-extension-gstreamer-pwcompat",
]

COMMON_PHOSH = [
	"phosh-config-hwcomposer",
]

# Common packages for phones
COMMON_PHONE_PACKAGES = [
	"adaptation-hybris-common",
	"ofono",
	"ofono-scripts",
	"ofono2mm",
	"mmsd4ofono",
	"mmsd4ofono-scripts",
]

# Devtools packages
COMMON_DEVTOOLS_PACKAGES = [
	"adaptation-hybris-common",
	"libhybris-test",
	"hybris-usb",
]

# Common packages for api levels 16+
COMMON_16_PACKAGES = [
	"adaptation-hybris-common",
	"pulseaudio-config-droid",
	"pipewire-config-droid",
	"furios-quirks-api%(level)d",
]

# Common packages for api levels 30+ (11+)
COMMON_30_PACKAGES = [
	"pulseaudio-modules-droid-modern",
]

# Common packages for api levels 26+ (8+)
COMMON_26_PACKAGES = [
	"bluebinder",
	"timekeeper",
]

# Common phone packages for api levels 26+ (8+)
COMMON_26_PHONE_PACKAGES = [
	"adaptation-hybris-common",
	"adaptation-hybris-phone",
	"adaptation-hybris-api%(level)s",
	"ofono-binder-plugin",
	"ofono-configs-binder-common",
	"pulseaudio-modules-droid-hidl",
	"audiosystem-passthrough",
]

# Common phone packages for dual sim devices for api levels 26+ (8+)
COMMON_26_DUAL_SIM_PACKAGES = [
	"adaptation-hybris-api%(level)d-phone",
	"ofono-configs-binder-dual-sim",
]

SUPPORTED_APILEVELS = {
	0 : {
		"common" : COMMON_PACKAGES,
		"phone"    : COMMON_PHONE_PACKAGES,
		"devtools" : COMMON_DEVTOOLS_PACKAGES,
		"phosh"    : COMMON_PHOSH,
	},
        32 : {
                "standard"       : COMMON_16_PACKAGES + COMMON_30_PACKAGES + COMMON_26_PACKAGES,
                "phone"          : COMMON_26_PHONE_PACKAGES,
                "phone-dual-sim" : COMMON_26_DUAL_SIM_PACKAGES,
        },
        33 : {
                "standard"       : COMMON_16_PACKAGES + COMMON_30_PACKAGES + COMMON_26_PACKAGES,
                "phone"          : COMMON_26_PHONE_PACKAGES,
                "phone-dual-sim" : COMMON_26_DUAL_SIM_PACKAGES,
        },
}

PROVIDES_TEMPLATE = """
Provides: adaptation-hybris-apispecific-%(variant)s
Conflicts: adaptation-hybris-apispecific-%(variant)s"""

TEMPLATE = """
Package: %(package)s
Architecture: any
Depends: %(depends)s
Description: %(summary)s
%(description)s
"""

if __name__ == "__main__":
	with open("debian/control.head", "r") as f:
		head = f.read()

	with open("debian/control", "w") as f:
		f.write(head)

		for level, variants in SUPPORTED_APILEVELS.items():
			for variant, depends in variants.items():
				subs = {
					"basepkg" : "adaptation-hybris-api%d" % level if level > 0 else "adaptation-hybris",
					"level" : level,
					"variant" : variant,
				}
				if level > 0:
					f.write(PROVIDES_TEMPLATE % {"variant" : variant})
				f.write(
					TEMPLATE % {
						"package" : "%(basepkg)s-%(variant)s" % subs if variant != "standard" else subs["basepkg"],
						"depends" : ",\n         ".join([dep % subs for dep in depends]),
						"summary" : "Base metapackage for %(basepkg)s adaptations (%(variant)s variant)" % subs,
						"description" : " This package depends on the required packages\n to allow FuriOS work on API %d devices." % level
						                if level > 0 else
						                " This package depends on the required packages\n to allow FuriOS work on Android devices."
					}
				)
