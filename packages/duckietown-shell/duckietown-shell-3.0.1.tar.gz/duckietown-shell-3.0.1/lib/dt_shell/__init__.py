# -*- coding: utf-8 -*-
import logging
import sys
import traceback

logging.basicConfig()

dtslogger = logging.getLogger('dts')
dtslogger.setLevel(logging.INFO)

import termcolor

__version__ = '3.0.1'

from .cli import DTShell

from .dt_command_abs import DTCommandAbs
from .dt_command_placeholder import DTCommandPlaceholder

dtslogger.info('duckietown-shell %s' % __version__)
dtslogger.info(
        'Please report problems with specific commands at https://github.com/duckietown/duckietown-shell-commands/issues/new')
dtslogger.info('Please report problems with the shell at https://github.com/duckietown/duckietown-shell/issues/new')


def cli_main():
    # TODO: register handler for Ctrl-C

    from dt_shell.env_checks import InvalidEnvironment

    shell = DTShell()
    arguments = sys.argv[1:]

    known_exceptions = (InvalidEnvironment,)

    try:
        if arguments:
            cmdline = " ".join(arguments)
            shell.onecmd(cmdline)
        else:
            shell.cmdloop()
    except known_exceptions as e:
        msg = str(e)
        termcolor.cprint(msg, 'yellow')
        sys.exit(1)
    except Exception as e:
        msg = traceback.format_exc(e)
        termcolor.cprint(msg, 'red')
        sys.exit(2)
