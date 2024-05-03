from argparse import ArgumentParser


class CLI:
    cli_description = """
            EVTX security logs viewer for Linux.

            Application designed specifically for Linux systems
            for more convenient, fast and efficient viewing
            Windows security logs in EVTX format.

            The application supports both graphical and
            console mode of operation, which allows everyone
            Optimize your workflow the way you need it.
        """

    def __init__(self):
        arg_parser = ArgumentParser(description=self.cli_description)
        self._setup_arguments(parser=arg_parser)

        self.arguments = arg_parser.parse_args()

    def __call__(self):
        print(self.arguments.file_path)

    @staticmethod
    def _setup_arguments(parser: ArgumentParser) -> None:
        parser.add_argument(
            "-f",
            "--file",
            required=True,
            help="path/to/file.evtx",
            dest="file_path",
            metavar="",
        )


start_cli = CLI()
