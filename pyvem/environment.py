import venv
import logging
import os
import shutil
import subprocess
import sys
import sysconfig
import types

import pyvem.config

logger = logging.Logger(__name__)
class Environment(venv.EnvBuilder):
    """Represents details about an environment, just acts as a setter/getter

    Attributes:
        prompt
        python_version
        with_pip
        upgrade
        symlinks
        clear
        system_site_packages
    """
    def __init__(
            self,
            prompt,
            python_version=None,
            with_pip=True,
            upgrade=False,
            symlinks=False,
            clear=False,
            system_site_packages=False
        ):
        """Gives every kwarg an attribute"""
        args = locals()
        args.pop('self')
        args.pop('__class__')
        self.python_version = args.pop('python_version')
        self.args = args
        self.__dict = dict(args)
        self.__dict['python_version'] = python_version
        super().__init__(**args)

    def _asdict(self):
        return self.__dict

    def create(self):
        path_ = pyvem.config.get_pyvem_home() / self.prompt
        super().create(path_)

    '''
    def create_configuration(self, context):
        """
        Create a configuration file indicating where the environment's Python
        was copied from, and whether the system site-packages should be made
        available in the environment.

        :param context: The information for the environment creation request
                        being processed.
        """
        context.cfg_path = path = os.path.join(context.env_dir, 'pyvenv.cfg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write('home = %s\n' % context.python_dir)
            if self.system_site_packages:
                incl = 'true'
            else:
                incl = 'false'
            f.write('include-system-site-packages = %s\n' % incl)
            f.write('version = %d.%d.%d\n' % sys.version_info[:3])
            if self.prompt is not None:
                f.write(f'prompt = {self.prompt!r}\n')

    if os.name != 'nt':
        def symlink_or_copy(self, src, dst, relative_symlinks_ok=False):
            """
            Try symlinking a file, and if that fails, fall back to copying.
            """
            force_copy = not self.symlinks
            if not force_copy:
                try:
                    if not os.path.islink(dst): # can't link to itself!
                        if relative_symlinks_ok:
                            assert os.path.dirname(src) == os.path.dirname(dst)
                            os.symlink(os.path.basename(src), dst)
                        else:
                            os.symlink(src, dst)
                except Exception:   # may need to use a more specific exception
                    logger.warning('Unable to symlink %r to %r', src, dst)
                    force_copy = True
            if force_copy:
                shutil.copyfile(src, dst)
    else:
        def symlink_or_copy(self, src, dst, relative_symlinks_ok=False):
            """
            Try symlinking a file, and if that fails, fall back to copying.
            """
            bad_src = os.path.lexists(src) and not os.path.exists(src)
            if self.symlinks and not bad_src and not os.path.islink(dst):
                try:
                    if relative_symlinks_ok:
                        assert os.path.dirname(src) == os.path.dirname(dst)
                        os.symlink(os.path.basename(src), dst)
                    else:
                        os.symlink(src, dst)
                    return
                except Exception:   # may need to use a more specific exception
                    logger.warning('Unable to symlink %r to %r', src, dst)

            # On Windows, we rewrite symlinks to our base python.exe into
            # copies of venvlauncher.exe
            basename, ext = os.path.splitext(os.path.basename(src))
            srcfn = os.path.join(os.path.dirname(__file__),
                                 "scripts",
                                 "nt",
                                 basename + ext)
            # Builds or venv's from builds need to remap source file
            # locations, as we do not put them into Lib/venv/scripts
            if sysconfig.is_python_build(True) or not os.path.isfile(srcfn):
                if basename.endswith('_d'):
                    ext = '_d' + ext
                    basename = basename[:-2]
                if basename == 'python':
                    basename = 'venvlauncher'
                elif basename == 'pythonw':
                    basename = 'venvwlauncher'
                src = os.path.join(os.path.dirname(src), basename + ext)
            else:
                src = srcfn
            if not os.path.exists(src):
                if not bad_src:
                    logger.warning('Unable to copy %r', src)
                return

            shutil.copyfile(src, dst)

    def setup_python(self, context):
        """
        Set up a Python executable in the environment.

        :param context: The information for the environment creation request
                        being processed.
        """
        binpath = context.bin_path
        path = context.env_exe
        copier = self.symlink_or_copy
        dirname = context.python_dir
        if os.name != 'nt':
            copier(context.executable, path)
            if not os.path.islink(path):
                os.chmod(path, 0o755)
            for suffix in ('python', 'python3'):
                path = os.path.join(binpath, suffix)
                if not os.path.exists(path):
                    # Issue 18807: make copies if
                    # symlinks are not wanted
                    copier(context.env_exe, path, relative_symlinks_ok=True)
                    if not os.path.islink(path):
                        os.chmod(path, 0o755)
        else:
            if self.symlinks:
                # For symlinking, we need a complete copy of the root directory
                # If symlinks fail, you'll get unnecessary copies of files, but
                # we assume that if you've opted into symlinks on Windows then
                # you know what you're doing.
                suffixes = [
                    f for f in os.listdir(dirname) if
                    os.path.normcase(os.path.splitext(f)[1]) in ('.exe', '.dll')
                ]
                if sysconfig.is_python_build(True):
                    suffixes = [
                        f for f in suffixes if
                        os.path.normcase(f).startswith(('python', 'vcruntime'))
                    ]
            else:
                suffixes = ['python.exe', 'python_d.exe', 'pythonw.exe',
                            'pythonw_d.exe']

            for suffix in suffixes:
                src = os.path.join(dirname, suffix)
                if os.path.lexists(src):
                    copier(src, os.path.join(binpath, suffix))

            if sysconfig.is_python_build(True):
                # copy init.tcl
                for root, dirs, files in os.walk(context.python_dir):
                    if 'init.tcl' in files:
                        tcldir = os.path.basename(root)
                        tcldir = os.path.join(context.env_dir, 'Lib', tcldir)
                        if not os.path.exists(tcldir):
                            os.makedirs(tcldir)
                        src = os.path.join(root, 'init.tcl')
                        dst = os.path.join(tcldir, 'init.tcl')
                        shutil.copyfile(src, dst)
                        break

    def _setup_pip(self, context):
        """Installs or upgrades pip in a virtual environment"""
        # We run ensurepip in isolated mode to avoid side effects from
        # environment vars, the current directory and anything else
        # intended for the global Python environment
        cmd = [context.env_exe, '-Im', 'ensurepip', '--upgrade',
                                                    '--default-pip']
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)

    def setup_scripts(self, context):
        """
        Set up scripts into the created environment from a directory.

        This method installs the default scripts into the environment
        being created. You can prevent the default installation by overriding
        this method if you really need to, or if you need to specify
        a different location for the scripts to install. By default, the
        'scripts' directory in the venv package is used as the source of
        scripts to install.
        """
        path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(path, 'scripts')
        print('possibly override this', path)
        self.install_scripts(context, path)

    def install_scripts(self, context, path):
        """
        Install scripts into the created environment from a directory.

        :param context: The information for the environment creation request
                        being processed.
        :param path:    Absolute pathname of a directory containing script.
                        Scripts in the 'common' subdirectory of this directory,
                        and those in the directory named for the platform
                        being run on, are installed in the created environment.
                        Placeholder variables are replaced with environment-
                        specific values.
        """
        print(path)
        binpath = context.bin_path
        plen = len(path)
        for root, dirs, files in os.walk(path):
            if root == path: # at top-level, remove irrelevant dirs
                for d in dirs[:]:
                    if d not in ('common', os.name):
                        dirs.remove(d)
                continue # ignore files in top level
            for f in files:
                if (os.name == 'nt' and f.startswith('python')
                        and f.endswith(('.exe', '.pdb'))):
                    continue
                srcfile = os.path.join(root, f)
                suffix = root[plen:].split(os.sep)[2:]
                if not suffix:
                    dstdir = binpath
                else:
                    dstdir = os.path.join(binpath, *suffix)
                if not os.path.exists(dstdir):
                    os.makedirs(dstdir)
                dstfile = os.path.join(dstdir, f)
                with open(srcfile, 'rb') as f:
                    data = f.read()
                if not srcfile.endswith(('.exe', '.pdb')):
                    try:
                        data = data.decode('utf-8')
                        data = self.replace_variables(data, context)
                        data = data.encode('utf-8')
                    except UnicodeError as e:
                        data = None
                        logger.warning('unable to copy script %r, '
                                       'may be binary: %s', srcfile, e)
                if data is not None:
                    with open(dstfile, 'wb') as f:
                        f.write(data)
                    shutil.copymode(srcfile, dstfile)
    '''
