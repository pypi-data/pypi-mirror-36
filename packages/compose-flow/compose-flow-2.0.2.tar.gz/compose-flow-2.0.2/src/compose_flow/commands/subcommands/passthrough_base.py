import argparse
import logging
import os

from distutils.spawn import find_executable

import sh

from .base import BaseSubcommand

from compose_flow import errors


class PassthroughBaseSubcommand(BaseSubcommand):
    command_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def fill_subparser(cls, parser, subparser) -> None:
        subparser.add_argument('extra_args', nargs=argparse.REMAINDER)

    def get_command(self):
        # check to make sure the command is installed
        command_path = find_executable(self.command_name)
        if command_path is None:
            raise errors.ErrorMessage(f'{self.command_name} not found in PATH; is it installed?')

        return [command_path]

    def handle(self, extra_args:list=None) -> [None, str]:
        command = self.get_command()

        extra_args = extra_args or self.args.extra_args
        command.extend(extra_args)

        self.logger.info(' '.join(command))

        if not self.args.dry_run:
            # os.execve(command[0], command, os.environ)
            proc = getattr(sh, command[0])
            proc(*command[1:], _env=os.environ, _fg=True)

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(f'{__name__}.{self.__class__.__name__}')
