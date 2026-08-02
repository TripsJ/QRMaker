"""Creating QR Codes via TUI, or commandline."""

import argparse
import os
import sys

import qrcode

# import ttkbootstrap as ttk als ansatz für die gui später


def create_qr(url: str, filename: str, overwrite: bool = False) -> None:
    """Create a file containing a qrcode.

    Args:
        url: the contend encoded into the qrcode.
        filename: the name of the created file.
        overwrite: a boolean defining wether or not to overwrite an exsisting file.

    Returns:
        None.

    Raises:
        FileExistsError if the File it Creates already exsists.

    """
    if os.path.isfile(filename) and not overwrite:
        raise FileExistsError
    else:
        qrcode.make(url).save(filename)  # type: ignore[arg-type]  # str-Pfad ist zur Laufzeit gültig, Stub ist zu eng


def remove_extension(name: str) -> str:
    """Remove everything behind the first . in a string.

    Args:
       name: a string representing a filename.

    Returns:
       Filename with everything after the first . removed.

    Raises:
       ValueError if String is empty after modification.

    """
    sep = "."
    stripped_filename = name.split(sep, 1)[0]
    if len(stripped_filename) < 1:
        raise ValueError
    else:
        return stripped_filename


def cmd_mode() -> None:
    """Take in arguments from the commandline and call create_qr.

    Args:
       None.

    Returns:
       None.

    Raises:
       Nothing.

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("link")
    args = parser.parse_args()
    if args.filename and args.link:
        overwrite = False
        try:
            f = remove_extension(args.filename)
            filename = f"{f}.png"
        except ValueError as e:
            print(f"""Invalid Filename specified\n
            The returned exception is {e}\n
            Exiting.""")
            sys.exit()
        while True:
            try:
                create_qr(args.link, filename, overwrite=overwrite)
                break
            except FileExistsError:
                print("The Given File Already exists\n")
                if input("Overwrite? (y/n): ").lower() == "y":
                    overwrite = True
                else:
                    print("User refused Overwrite. Exiting")
                    sys.exit()
            except OSError as e:
                print(f"""The specified file could not be created.\n
                The returned Error is {e}\n
                Exiting""")
                sys.exit()


def text_mode() -> None:
    """Ask User for values on the Commandline and calls create_qr.

    Args:
       None.

    Returns:
       None.

    Raises:
       Nothing.

    """
    # taking user input
    url = input("give me a link: ")
    filename = input("give me a filename: ")
    # removing anything after a . so there arent double file extensions
    try:
        str_name = remove_extension(filename)
    except ValueError:
        print("no filename specified, Abandonning")
        sys.exit()
    if not url:  # empty strings are falsy
        print("this would create an empty qr code. Abandonning")
        sys.exit()

    target = f"{str_name}.png"
    overwrite = False
    while True:
        try:
            create_qr(url, target, overwrite)
            break
        except FileExistsError:
            print("The Given File Already exists\n")
            if input("Overwrite? (y/n): ").lower() == "y":
                overwrite = True
            else:
                print("User refused Overwrite. Exiting")
                sys.exit()
        except OSError as e:
            print(f"""The specified file could not be created.\n
            The returned Error is {e}\n
            Exiting""")
            sys.exit()


def main() -> None:
    """Execute the program and decide what mode should be used.

    Args:
       None.

    Returns:
       None.

    Raises:
       Nothing.

    """
    if len(sys.argv) == 1:
        text_mode()
    else:
        cmd_mode()


if __name__ == "__main__":
    main()
