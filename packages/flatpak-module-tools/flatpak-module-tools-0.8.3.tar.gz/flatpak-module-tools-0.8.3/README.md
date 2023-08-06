About
=====
flatpak-module-tools is a set of command line tools (all accessed via a single
'flatpak-module' executable) for operations related to maintaining Flatpak
applications and runtimes as Fedora modules.

flatpak-module local-build
==========================
The `flatpak-module local-build` builds the module locally, then creates a flatpak of it.
It is equivalent to running `flatpak-module build-module; flatpak-module build-container --source=local`

Usage:
    flatpak-module local-build
	     [--add-local-build=NAME:STREAM[:VERSION]]
		 [--modulemd=mymodule.yaml]
		 [--containerspec=somedir/container.yaml]
		 [--stream=STREAM]
	     [--install]

**--add-local-build**
include a local MBS module build as a source for the build

**--modulemd**
modulemd file to build. If in a git repository, defaults to <reponame>.yaml

**--containerspec**
path to container.yaml - defaults to `./container.yaml`

**--stream**
Module stream for the build. If in a git repository, defaults to `<branchname>`

**--install**
automatically install the resulting Flatpak or runtime for the current user

flatpak-module build-module
===========================
A wrapper around `mbs-manager build_module_locally`.

Usage:
    flatpak-module build-module
	     [--add-local-build=NAME:STREAM[:VERSION]]
		 [--modulemd=mymodule.yaml]
		 [--stream=STREAM]

**--add-local-build**
include a local MBS module build  as a source for the build

**--modulemd**
modulemd file to build. If in a git repository, defaults to `<reponame>.yaml`

**--stream**
Module stream for the build. If in a git repository, defaults to `<branchname>`

flatpak-module build-container
==============================
Creates a OCI container of an Flatpak application or runtime from a module build.

Output file is:

 NAME-STREAM-VERSION-oci.tar.gz

For example:

 org.example.MyApp-stable-20180205192824.oci.tar.gz

Usage:
    flatpak-module build-container
	     [--add-local-build=NAME:STREAM[:VERSION]]
	     [--from-local]
	     [--install/--install-user]
		 [--containerspec=somedir/container.yaml]

**--add-local-build**
include a local MBS module build  as a source for the build

**--from-local**
Specifies to build the container from a local module build. Shorthand for '--add-local-build=NAME:STREAM' with the name and stream from container.yaml.

**--install**
automatically install the resulting Flatpak or runtime systemwide

**--containerspec**
path to container.yaml - defaults to `./container.yaml`

flatpak-module install
======================

Installs a Flatpak or Runtime built as an OCI bundle.

Usage:
    flatpak-module install [PATH-or-URL]

**--install**
install the resulting Flatpak for the current user. If it doesn't already exist, a
`flatpak-module-tools` remote is added to the Flatpak's user configuration.

LICENSE
=======
flatpak-module-tools is licensed under the MIT license. See the LICENSE file for details.
