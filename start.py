from argparse import ArgumentParser

# TODO: Remove stubs, organize calling of necessary modules.
launch_mode = {
    "CLI": print,
    "GUI": print,
}


def setup_mode_argument(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--mode",
        default="CLI",
        help="specifies in which mode the program should be launched (CLI/GUI). Default CLI.",
        choices=("CLI", "GUI"),
        metavar="",
    )


def main() -> None:
    arg_parser = ArgumentParser(
        description="""
            EVTX security logs viewer for Linux. \n

            Application designed specifically for Linux systems
            for more convenient, fast and efficient viewing
            Windows security logs in EVTX format.

            The application supports both graphical and
            console mode of operation, which allows everyone
            Optimize your workflow the way you need it.
        """
    )

    setup_mode_argument(parser=arg_parser)
    launch_args = arg_parser.parse_args()

    input_mode = launch_args.mode.upper()
    mode = launch_mode[input_mode]

    mode()


if __name__ == "__main__":
    main()
