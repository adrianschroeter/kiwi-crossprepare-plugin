import sys

from mock import (
    Mock, patch
)
from kiwi_crossprepare_plugin.tasks.system_crossprepare import SystemCrossprepareTask


class TestSystemCrossprepareTask:
    def setup(self):
        sys.argv = [
            sys.argv[0],
            'system', 'crossprepare',
            '--init', '/some/qemu/binfmt/init',
            '--target-arch', 'x86_64',
            '--target-dir', '../data/target_dir'
        ]
        self.task = SystemCrossprepareTask()

    def _init_command_args(self):
        self.task.command_args = {}
        self.task.command_args['help'] = False
        self.task.command_args['crossprepare'] = False
        self.task.command_args['--target-arch'] = 'x86_64'
        self.task.command_args['--init'] = '/some/qemu/binfmt/init'
        self.task.command_args['--allow-existing-root'] = False
        self.task.command_args['--target-dir'] = '../data/target_dir'

    @patch('kiwi_crossprepare_plugin.tasks.system_crossprepare.Help')
    def test_process_system_crossprepare_help(self, mock_kiwi_Help):
        Help = Mock()
        mock_kiwi_Help.return_value = Help
        self._init_command_args()
        self.task.command_args['help'] = True
        self.task.command_args['crossprepare'] = True
        self.task.process()
        Help.show.assert_called_once_with(
            'kiwi::system::crossprepare'
        )
