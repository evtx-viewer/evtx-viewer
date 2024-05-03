from argparse import ArgumentParser
from parser import parse_records


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
        arg_parser = ArgumentParser(description=self.cli_description)
        self._setup_arguments(parser=arg_parser)

        self.arguments = arg_parser.parse_args()

    # TODO: Write me
    def __call__(self) -> None:
        records = parse_records(input_path=self.arguments.input_path)

        if self.arguments.output_path:
            with open(self.arguments.output_path, "w") as output_file:
                # write to file
                pass

        else:
            records.print_all()

    @staticmethod
    def _setup_arguments(parser: ArgumentParser) -> None:
        parser.add_argument(
            "-f",
            "--file",
            required=True,
            help="input path/to/file.evtx",
            dest="input_path",
            metavar="",
        )
        parser.add_argument(
            "-o",
            "--output",
            required=False,
            help="output path/to/file.txt",
            dest="output_path",
            metavar="",
        )


start_cli = CLI()
