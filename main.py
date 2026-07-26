import qrcode


def create_qr(url: str, filename: str):
    qrcode.make(url).save(filename)


def main():
    # taking user input
    url = input("give me a link: ")
    filename = input("give me a filename: ")
    # removing anything after a . so therearent double fileextensions

    sep = "."
    stripped_filename = filename.split(sep, 1)[0]
    try:
        create_qr(url, f"{stripped_filename}.png")
    except FileNotFoundError:
        print("The specified file could not be created. Did you set a filename?")
        main()


if __name__ == "__main__":
    main()
