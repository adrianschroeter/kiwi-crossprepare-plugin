KIWI - Cross Image Arch Prepare Plugin
======================================

.. |GitHub CI Action| image:: https://github.com/OSInside/kiwi-crossprepare-plugin/workflows/CILint/badge.svg
   :target: https://github.com/OSInside/kiwi-crossprepare-plugin/actions

|GitHub CI Action|

KIWI plugin to prepare an image root tree for a cross architecture build process.
Building an image for a different architecture than the host architecture
can be done in several ways. One way is to emulate a virtual machine
of the target architecture using the `boxbuild` command. However, that
emulation is not very fast. A faster but also more complex approach
is to provide binary emulation in userspace. This plugin prepares a
new image target directory with all data needed to run applications
for the image target architecture using the QEMU User Emulation
feature.
