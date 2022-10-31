from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

def main(name):
    file_path = 'public/file.pdf'

    with open(file_path, "rb") as file:
        file_data = file.read()

    try:
        key = RSA.import_key(open('keys/' + name + '/private.pem').read())
        h = SHA256.new(file_data)
        signature = pss.new(key).sign(h)

        signature_path = 'public/file.pdf.sig'
        with open(signature_path, "wb") as file:
            file.write(signature)
    except FileNotFoundError:
        print("No key found for " + name)
        print("Please generate a key first")

if __name__ == '__main__':
    name = input("Enter your name: ")
    main(name)