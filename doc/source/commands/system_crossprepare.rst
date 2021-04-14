kiwi-ng system crossprepare
===========================

SYNOPSIS
--------

.. code:: bash

   kiwi-ng [global options] service <command> [<args>]

   kiwi-ng system crossprepare -h | --help
   kiwi-ng system crossprepare --target-arch=<arch> --init=<name> --target-dir=<directory>
       [--allow-existing-root]
   kiwi-ng system crossprepare help

DESCRIPTION
-----------

Prepare an image root tree for a cross architecture build process.
Building an image for a different architecture than the host architecture
can be done in several ways. One way is to emulate a virtual machine
of the target architecture using the `boxbuild` command. However, that
emulation is not very fast. A faster but also more complex approach
is to provide binary emulation in userspace. This plugin prepares a
new image target directory with all data needed to run applications
for the image target architecture using the QEMU User Emulation
feature.

The process to build an image cross arch using the crossprepare plugin
is two fold. First the image target directory gets prepared by a
`kiwi-ng system crossprepare` command call. Next the image for the target
architecture is build by a `kiwi-ng system build` command call.
Both commands specifies the target architecture via the `--target-arch`
parameter.


OPTIONS
-------

--target-arch=<arch>

  Name of image target architecture

--init=<name>

  Path to the image target architecture init program. The crossprepare plugin
  was created to support the qemu-binfmt concept to support calling cross-arch
  binaries. The preparation of an environment must be done by an independent
  host arch compatible binary which we call `init program` as it will be used
  as PID 1 program in the QEMU call from which binaries of the image
  architecture can be called. Neither {kiwi} nor this plugin are providers
  of the init sequence because this implements a custom initialization
  procedure which does not follow standards. From the plugin code the
  provided binary will be called and trusted to do the right thing.
  
--target-dir=<directory>

  Path to store the build results. The crossprepare command will initialize
  a new root directory at `<directory>/image-root/` which is compatible to
  how the {kiwi} `build` command does it. Therefore the specified `--target-dir`
  argument here can also be used for a subsequent `build` command.
  
--allow-existing-root

  Allow to use an existing root directory from an earlier
  preparation attempt.


EXAMPLE
-------

.. code:: bash

   $ kiwi-ng system crossprepare --target-arch aarch64 \
       --init /usr/lib/build/initvm.aarch64
       --target-dir /tmp/myimage
