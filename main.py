import sys
from os import path
import qrcode
import ttkbootstrap as ttk


def create_qr(url: str, filename: str, overwrite: bool = False):
    if path.isfile(filename) and overwrite == False:
        raise FileExistsError
    else:
        qrcode.make(url).save(filename)


def remove_extension(name: str) -> str:
    sep = "."
    stripped_filename = name.split(sep, 1)[0]
    if len(stripped_filename) < 1:
        raise FileNotFoundError
    else:
        return stripped_filename


def text_mode():
    # taking user input
    url = input("give me a link: ")
    filename = input("give me a filename: ")
    # removing anything after a . so therearent double fileextensions
    try:
        str_name = remove_extension(filename)
    except FileNotFoundError:
        print("no filename specified, Abandonning")
        sys.exit()
    try:
        create_qr(url, f"{str_name}.png")
    except FileNotFoundError:
        print("The specified file could not be created.")
    except FileExistsError:
        print("The Given File Already exists\n")
        if input("Overwrite? (y/n): ").lower() == "y":
            try:
                create_qr(url, f"{str_name}.png", overwrite=True)
            except FileNotFoundError:
                print("The specified file could not be created. Exiting")
                sys.exit()
        else:
            print("User refused Overwrite. Exiting")
            sys.exit()


def main():
    text_mode()


if __name__ == "__main__":
    main()
