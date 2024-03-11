#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Eugenio "g7" Paolantonio <me@medesimo.eu>

# TODO: Maybe use python-debian?

# Common packages for every api level
COMMON_PACKAGES = [
	"droidian-quirks-writable-image",
	"android-base-passwd",
	"android-base-files",
	"udev",
	"lxc-android",
	"libhybris",
	"libhybris-utils",
	"udev-config-hybris",
	"hadess-sensorfw-proxy",
	"droidian-quirks-hybris-gl",
	"droidian-quirks-qt-force-gles",
	"droidian-quirks-tls-padding",
	"droidian-quirks-xtables-legacy",
	"gstreamer1.0-droid",
	"package-sideload",
	"flash-bootimage",
	"droidian-quirks-device",
	"flashlightd",
	"flatpak-hybris",
	"flatpak-extension-gl-hybris",
	"flatpak-extension-gl-hybris-tls-padding",
	"flatpak-extension-gl-hybris-droidian-workarounds",
]

COMMON_PHOSH = [
	"phosh-config-hwcomposer",
]

# Common packages for phones
COMMON_PHONE_PACKAGES = [
	"adaptation-hybris-common (= ${binary:Version})",
	"ofono",
	"ofono-scripts",
	"ofono2mm",
	"ofono-apndb-plugin",
	"lineageos-apn-conf",
]

# Devtools packages
COMMON_DEVTOOLS_PACKAGES = [
	"adaptation-hybris-common (= ${binary:Version})",
	"libhybris-test",
	"hybris-usb",
]

# Common packages for api levels 16+
COMMON_16_PACKAGES = [
	"adaptation-hybris-common (= ${binary:Version})",
	"pulseaudio-config-droid",
	"droidian-quirks-api%(level)d",
]

# Common packages for api levels 16 through 29 (4.1 to 29)
COMMON_16_29_PACKAGES = [
	"pulseaudio-modules-droid-jb2q",
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
	"adaptation-hybris-common (= ${binary:Version})",
	"adaptation-hybris-phone (= ${binary:Version})",
	"adaptation-hybris-api%(level)s (= ${binary:Version})",
	"ofono-ril-binder-plugin",
	"ofono-config-ril-binder",
	"pulseaudio-modules-droid-hidl",
	"audiosystem-passthrough",
]

# Common phone packages for dual sim devices for api levels 26+ (8+)
COMMON_26_DUAL_SIM_PACKAGES = [
	"adaptation-hybris-api%(level)d-phone (= ${binary:Version})",
	"ofono-config-ril-binder-dual-sim",
]

SUPPORTED_APILEVELS = {
	0 : {
		"common" : COMMON_PACKAGES,
		"phone"    : COMMON_PHONE_PACKAGES,
		"devtools" : COMMON_DEVTOOLS_PACKAGES,
		"phosh"    : COMMON_PHOSH,
	},
	28 : {
		"standard"       : COMMON_16_PACKAGES + COMMON_16_29_PACKAGES + COMMON_26_PACKAGES,
		"phone"          : COMMON_26_PHONE_PACKAGES,
		"phone-dual-sim" : COMMON_26_DUAL_SIM_PACKAGES,
	},
	29 : {
		"standard"       : COMMON_16_PACKAGES + COMMON_16_29_PACKAGES + COMMON_26_PACKAGES,
		"phone"          : COMMON_26_PHONE_PACKAGES,
		"phone-dual-sim" : COMMON_26_DUAL_SIM_PACKAGES,
	},
	30 : {
		"standard"       : COMMON_16_PACKAGES + COMMON_30_PACKAGES + COMMON_26_PACKAGES,
		"phone"          : COMMON_26_PHONE_PACKAGES,
		"phone-dual-sim" : COMMON_26_DUAL_SIM_PACKAGES,
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
						"description" : " This package depends on the required packages\n to allow Droidian work on API %d devices." % level
						                if level > 0 else
						                " This package depends on the required packages\n to allow Droidian work on Android devices."
					}
				)
