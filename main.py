import os
import sys

import qrcode

# import ttkbootstrap as ttk als ansatz für die gui später


def create_qr(url: str, filename: str, overwrite: bool = False) -> None:
    if os.path.isfile(filename) and not overwrite:
        raise FileExistsError
    else:
        qrcode.make(url).save(filename)  # type: ignore[arg-type]  # str-Pfad ist zur Laufzeit gültig, Stub ist zu eng


def remove_extension(name: str) -> str:
    sep = "."
    stripped_filename = name.split(sep, 1)[0]
    if len(stripped_filename) < 1:
        raise ValueError
    else:
        return stripped_filename


def text_mode() -> None:
    # taking user input
    url = input("give me a link: ")
    filename = input("give me a filename: ")
    # removing anything after a . so there arent double file extensions
    try:
        str_name = remove_extension(filename)
    except ValueError:
        print("no filename specified, Abandonning")
        sys.exit()
    if url == "":
        print("this would create an empty qr code. Abandonning")
        sys.exit()

        target = f"{str_name}.png"
        overwrite = False
    while True:
        try:
            create_qr(url, target, overwrite)

        except FileExistsError:
            print("The Given File Already exists\n")
            if input("Overwrite? (y/n): ").lower() == "y":
                overwrite = True
            else:
                print("User refused Overwrite. Exiting")
                sys.exit()
        except FileNotFoundError:
            print("The specified file could not be created. Exiting")
            sys.exit()


def main() -> None:
    text_mode()


if __name__ == "__main__":
    main()
