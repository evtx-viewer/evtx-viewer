import sys

# TODO: Remove stubs, organize calling of necessary modules.
launch_mode = {
    "CLI": print,
    "GUI": print,
}


def main() -> None:
    if len(sys.argv) < 2:
        raise RuntimeError("Need to specify the application launch mode.")

    input_mode = sys.argv[1].upper()
    mode = launch_mode.get(input_mode, "undefined")

    if mode == "undefined":
        raise RuntimeError(
            f'The application cannot be launched in "{input_mode}" mode.'
        )

    mode()


if __name__ == "__main__":
    main()
