
import os

from pex.bin.pex import main as pex_main
from pip._internal import main as pip_main

from pickley import CaptureOutput, system
from pickley.settings import SETTINGS


def add_paths(result, env_var, *paths):
    """
    :param dict result: Where to add path customization
    :param str env_var: Env var to customize
    :param list *paths: Paths to add, if corresponding folder exists
    """
    added = 0
    current = os.environ.get(env_var, "")
    if current:
        current = current.split(":")
    else:
        current = []
    current = [x for x in current if x]
    for path in paths:
        if os.path.isdir(path) and path not in current:
            added += 1
            current.append(path)
    if added:
        result[env_var] = ":".join(current)


class Runner:
    def __init__(self, cache):
        """
        :param str cache: Path to folder to use as cache
        """
        self.name = self.__class__.__name__.replace("Runner", "").lower()
        self.cache = cache

    def run(self, *args):
        args = system.flattened([self.prelude_args(), args], unique=False)

        if system.dryrun:
            system.debug("Would run: %s %s", self.name, system.represented_args(args))
            return None

        system.ensure_folder(self.cache, folder=True)
        system.debug("Running %s %s", self.name, system.represented_args(args))
        with CaptureOutput(self.cache, env=self.custom_env()) as captured:
            try:
                exit_code = self.effective_run(args)
            except SystemExit as e:
                exit_code = e.code
            if exit_code:
                return str(captured)
            return None

    def custom_env(self):
        """
        :return dict: Optional customized env vars to use
        """

    def effective_run(self, args):
        """
        :param list args: Args to run with
        :return int: Exit code
        """

    def prelude_args(self):
        """
        :return list|None: Arguments to pass to invoked module for all invocations
        """


class PipRunner(Runner):
    def effective_run(self, args):
        """
        :param list args: Args to run with
        :return int: Exit code
        """
        return pip_main(args)

    def prelude_args(self):
        """
        :return list|None: Arguments to pass to invoked module for all invocations
        """
        return ["--disable-pip-version-check", "--cache-dir", self.cache]

    def wheel(self, *package_names):
        return self.run("wheel", "-i", SETTINGS.index, "--wheel-dir", self.cache, *package_names)


class PexRunner(Runner):
    def custom_env(self):
        """
        :return dict: Optional customized env vars to use
        """
        result = {}
        add_paths(result, "PKG_CONFIG_PATH", "/usr/local/opt/openssl/lib/pkgconfig")
        return result

    def effective_run(self, args):
        """
        :param list args: Args to run with
        :return int: Exit code
        """
        return pex_main(args)

    def prelude_args(self):
        """
        :return list|None: Arguments to pass to invoked module for all invocations
        """
        return ["--no-pypi", "--cache-dir", self.cache, "--repo", self.cache]

    def is_universal(self, package_name, version):
        """
        :param str package_name: Pypi package name
        :param str version: Specific version of 'package_name' to examine
        :return bool: True if wheel exists and is universal
        """
        if not os.path.isdir(self.cache):
            return False
        prefix = "%s-%s-" % (package_name, version)
        for fname in os.listdir(self.cache):
            if fname.startswith(prefix) and fname.endswith(".whl"):
                return "py2.py3-none" in fname
        return False

    def resolved_python(self, package_name):
        """
        :param str package_name: Pypi package name
        :return pickley.settings.Definition: Associated definition
        """
        return SETTINGS.resolved_definition("python", package_name=package_name)

    def build(self, script_name, package_name, version, destination):
        """
        :param str script_name: Entry point name
        :param str package_name: Pypi package name
        :param str version: Specific version of 'package_name' to use
        :param str destination: Path where to generate pex
        :return str|None: None if successful, problem description otherwise
        """
        system.delete_file(destination)
        python = self.resolved_python(package_name)
        args = ["-c%s" % script_name, "-o%s" % destination, "%s==%s" % (package_name, version)]

        # Note: 'python.source' being 'SETTINGS.defaults' is the same as it being 'system.python'
        # Writing it this way is easier to change in tests
        explicit_python = python and python.value and python.source is not SETTINGS.defaults
        if explicit_python:
            shebang = python.value
            args.append("--python=%s" % python.value)

        elif not python or self.is_universal(package_name, version):
            shebang = "python"

        else:
            shebang = python.value

        if shebang:
            if not os.path.isabs(shebang):
                shebang = "/usr/bin/env %s" % shebang
            args.append("--python-shebang=%s" % shebang)

        return self.run(args)
