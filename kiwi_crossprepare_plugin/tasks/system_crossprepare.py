# Copyright (c) 2020 SUSE Software Solutions Germany GmbH.  All rights reserved.
#
# This file is part of kiwi-crossprepare-build.
#
# kiwi-crossprepare-build is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# kiwi-crossprepare-build is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kiwi-crossprepare-build.  If not, see <http://www.gnu.org/licenses/>
#
"""
usage: kiwi-ng system crossprepare -h | --help
       kiwi-ng system crossprepare --target-arch=<arch> --init=<name> --target-dir=<directory>
           [--allow-existing-root]
       kiwi-ng system crossprepare help

commands:
    crossprepare
        prepare an image root tree for a cross architecture build process

options:
    --target-arch=<arch>
        name of image target architecture
    --init=<name>
        path to the image target architecture init program.
        The crossprepare plugin was created to support the qemu-binfmt
        concept to support calling cross-arch binaries. The preparation
        of an environment must be done by an independent host arch
        compatible binary which we call `init program` as it will be
        used as PID 1 program in the QEMU call from which binaries of
        the image architecture can be called. Neither kiwi nor this
        plugin are providers of the init sequence because this
        implements a custom initialization procedure which does not
        follow standards. From the plugin code the provided binary will
        be called and trusted to do the right thing.
    --target-dir=<directory>
        path to store the build results. The crossprepare command will
        initialize a new root directory at <directory>/image-root/
        which is compatible to how the kiwi build command does it.
        Therefore the specified --target-dir argument can also be
        used for a subsequent kiwi build command.
    --allow-existing-root
        allow to use an existing root directory from an earlier
        preparation attempt.
"""
import logging
from kiwi.tasks.base import CliTask
from kiwi.help import Help

log = logging.getLogger('kiwi')


class SystemCrossprepareTask(CliTask):
    def process(self) -> None:
        self.manual = Help()
        if self.command_args.get('help') is True:
            return self.manual.show('kiwi::system::crossprepare')
