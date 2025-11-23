import qrcode

def generate_qr(text):
    img = qrcode.make(text)
    img.save("qrcode.png")
    print("QR Code saved as qrcode.png")

if __name__ == "__main__":
    text = input("Enter text/URL: ")
    generate_qr(text)
