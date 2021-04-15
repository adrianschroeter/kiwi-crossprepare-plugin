import sys
import io
from pytest import raises
from mock import (
    Mock, patch, call, MagicMock
)
from kiwi_crossprepare_plugin.tasks.system_crossprepare import SystemCrossprepareTask

from kiwi.exceptions import (
    KiwiFileNotFound,
    KiwiRootDirExists
)


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

    @patch('os.path.isfile')
    def test_process_raises_init_binary_not_found(self, mock_path_isfile):
        mock_path_isfile.return_value = False
        self.task.command_args['crossprepare'] = True
        with raises(KiwiFileNotFound):
            self.task.process()

    @patch('os.path.isfile')
    @patch('os.path.isdir')
    def test_process_raises_target_dir_exists(
        self, mock_path_isdir, mock_path_isfile
    ):
        mock_path_isfile.return_value = True
        mock_path_isdir.return_value = True
        self.task.command_args['crossprepare'] = True
        with raises(KiwiRootDirExists):
            self.task.process()

    @patch('shutil.copy')
    @patch('os.chmod')
    @patch('kiwi_crossprepare_plugin.tasks.system_crossprepare.TemporaryDirectory')
    @patch('kiwi_crossprepare_plugin.tasks.system_crossprepare.Path.create')
    @patch('kiwi_crossprepare_plugin.tasks.system_crossprepare.Command.run')
    @patch('os.path.isfile')
    @patch('os.path.isdir')
    @patch('os.path.exists')
    @patch('yaml.dump')
    def test_process(
        self, mock_yaml_dump, mock_os_path_exists, mock_os_path_isdir,
        mock_os_path_isfile, mock_Command_run, mock_Path_create,
        mock_TemporaryDirectory, mock_os_chmod, mock_shutil_copy
    ):
        mock_os_path_isdir.return_value = False
        init_dir = Mock()
        init_dir.name = '/tmp/initvm_X'
        mock_TemporaryDirectory.return_value = init_dir
        self._init_command_args()
        self.task.command_args['crossprepare'] = True
        self.task.command_args['--allow-existing-root'] = True

        mock_os_path_exists.return_value = False
        with raises(KiwiFileNotFound):
            self.task.process()

        mock_TemporaryDirectory.reset_mock()
        mock_shutil_copy.reset_mock()
        mock_Path_create.reset_mock()
        mock_os_path_exists.return_value = True
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=io.IOBase)
            file_handle = mock_open.return_value.__enter__.return_value
            self.task.process()
            mock_yaml_dump.assert_called_once_with(
                {
                    'exclude': [
                        '/usr/bin/qemu-binfmt',
                        '/usr/bin/qemu-x86_64-binfmt',
                        '/usr/bin/qemu-x86_64'
                    ]
                }, file_handle
            )

        mock_TemporaryDirectory.assert_called_once_with(
            prefix='initvm_'
        )
        assert mock_shutil_copy.call_args_list == [
            call('/some/qemu/binfmt/init', '/tmp/initvm_X'),
            call(
                '/usr/bin/qemu-binfmt',
                '../data/target_dir/build/image-root/usr/bin'
            ),
            call(
                '/usr/bin/qemu-x86_64-binfmt',
                '../data/target_dir/build/image-root/usr/bin'
            ),
            call(
                '/usr/bin/qemu-x86_64',
                '../data/target_dir/build/image-root/usr/bin'
            )
        ]
        assert mock_Path_create.call_args_list == [
            call('../data/target_dir/build/image-root/usr/bin'),
            call('../data/target_dir/build/image-root/image')
        ]
        mock_Command_run.assert_called_once_with(
            ['/tmp/initvm_X/init']
        )
