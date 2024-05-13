from pathlib import Path
import sys
from typing import Optional, List, Union


# TODO: write me
def validate_input(path: str) -> Optional[Union[str, List[str]]]:
    try:
        path_object: Path = Path(path)
        if path_object.is_dir():
            files: List[str] = list(path_object.glob("*.evtx"))
            if not files:
                raise FileNotFoundError(
                    "Not a single EVTX security log was found in the directory."
                )

            return [ptf.resolve().as_posix() for ptf in files]

        elif path_object.is_file():
            extension: str = path_object.suffix
            if extension != ".evtx":
                raise ValueError("The file is not an EVTX security log.")

            return path_object.resolve().as_posix()

        else:
            raise ValueError("This is not a file or a directory.")

    except (ValueError, FileNotFoundError) as error:
        sys.stdout.write(str(error) + "\n")
        return None
