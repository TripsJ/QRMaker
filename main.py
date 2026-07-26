import qrcode
import sys


def create_qr(url: str, filename: str):
    qrcode.make(url).save(filename)


def main():
    # taking user input
    url = input("give me a link: ")
    filename = input("give me a filename: ")
    # removing anything after a . so therearent double fileextensions
    try:
        sep = "."
        stripped_filename = filename.split(sep, 1)[0]
        if len(stripped_filename) <1:
            raise FileNotFoundError
    except FileNotFoundError:
        print("no filename specified, Abandonning")
        sys.exit()
    try:
        create_qr(url, f"{stripped_filename}.png")
    except FileNotFoundError:
        print("The specified file could not be created.")
        
    

if __name__ == "__main__":
    main()
