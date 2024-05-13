import sys
from argparse import ArgumentParser
from parser import parse_records
from typing import List, NamedTuple
import path
import config


class CLI(object):
    """
    docstring
    """

    cli_description = """
        EVTX security logs viewer for Linux.

        Application designed specifically for Linux systems
        for more convenient, fast and efficient viewing
        Windows security logs in EVTX format.

        The application supports both graphical and
        console mode of operation, which allows everyone
        Optimize your workflow the way you need it.
    """

    def __init__(self) -> None:
        self.arg_parser = ArgumentParser(description=self.cli_description)
        self.__configure_arguments(arg_names=["file", "output"])

        self.arguments = self.arg_parser.parse_args()

    # TODO: Write me
    def __call__(self) -> None:
        # TODO: write f\o path validation.
        result = path.validate_input(self.arguments.input_path)
        sys.stdout.write(str(result))

    def __configure_arguments(self, arg_names: List[str]) -> None:
        for arg_name in arg_names:
            arg_data: NamedTuple = config.cli_arguments.get_arg_data(arg_name)
            self.arg_parser.add_argument(
                arg_data.short_flag,
                arg_data.long_flag,
                required=arg_data.required,
                help=arg_data.description,
                dest=arg_data.aliase,
                metavar=arg_data.metavar,
                default=arg_data.default,
            )


start_cli = CLI()
