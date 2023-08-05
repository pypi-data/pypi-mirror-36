import os

from .env_command import EnvCommand


class DevelopCommand(EnvCommand):
    """
    Installs the current project in development mode.

    develop
    """

    help = """\
The <info>develop</info> command installs the current project in development mode.
"""

    def handle(self):
        from poetry.masonry.builders import SdistBuilder
        from poetry.io import NullIO
        from poetry.utils._compat import decode
        from poetry.utils.env import NullEnv

        setup = self.poetry.file.parent / "setup.py"
        has_setup = setup.exists()

        if has_setup:
            self.line("<warning>A setup.py file already exists. Using it.</warning>")
        else:
            builder = SdistBuilder(self.poetry, NullEnv(), NullIO())

            with setup.open("w") as f:
                f.write(decode(builder.build_setup()))

        try:
            self._install(setup)
        finally:
            if not has_setup:
                os.remove(str(setup))

    def _install(self, setup):
        self.call("install")

        self.line(
            "Installing <info>{}</info> (<comment>{}</comment>)".format(
                self.poetry.package.pretty_name, self.poetry.package.pretty_version
            )
        )
        self.env.run("pip", "install", "-e", str(setup.parent), "--no-deps")
