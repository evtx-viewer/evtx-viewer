from pathlib import Path
from typing import (
    Optional,
    List,
)


# TODO: write me
def validate_input(path: str) -> Optional[str | List[str]]:
    path_object: Path = Path(path)
    if path_object.is_dir():
        files: List[str] = list(path_object.glob("*.evtx"))
        if not files:
            raise FileNotFoundError(
                "Not a single EVTX security log was found in the directory."
            )

        return files

    elif path_object.is_file():
        extension: str = path_object.suffix()
        if extension != "evtx":
            raise ValueError("The file is not an EVTX security log.")

        return path
