from typing import NamedTuple


class Argument(NamedTuple):
    short_flag: str
    long_flag: str
    required: bool
    description: str
    aliase: str | None
    metavar: str | None
    default: str | int | None
    # add an other properties if you need


class CLIArgs(object):
    def __init__(self) -> None:
        self.file = Argument(
            short_flag="-f",
            long_flag="--file",
            required=True,
            description="input path/to/file.evtx",
            aliase="input_path",
            metavar="",
            default=None,
        )
        self.output = Argument(
            short_flag="-o",
            long_flag="--output",
            required=False,
            description="output path/to/file.txt",
            aliase="output_path",
            metavar="",
            default="./",
        )
        self.output = Argument(
            short_flag="-p",
            long_flag="--print",
            required=False,
            description="displays the result of viewing the file into a stdout flow",
            aliase="print",
            metavar="",
            default="",
        )

    def get_arg_data(self, arg_name: str) -> NamedTuple:
        return getattr(self, arg_name)
