import qrcode

def create_qr(url:str,filename:str):
    qrcode.make(url).save(filename)

def main ():
    url = input("give me a link: ")
    filename = input("give me a filename: ")
    create_qr(url,filename)
    
if __name__=="__main__" :
    main()
    
