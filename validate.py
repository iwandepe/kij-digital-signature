from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

def main(name):
    file_path = 'public/file.pdf'

    with open(file_path, "rb") as file:
        file_data = file.read()

    try:
        key = RSA.import_key(open('keys/' + name +'/public.pem').read())
        h = SHA256.new(file_data)
        verifier = pss.new(key)

        try:
            with open('public/file.pdf.sig', "rb") as signature_file:
                signature = signature_file.read()
                verifier.verify(h, signature)
                print("The signature is authentic.")
        except (ValueError, TypeError):
            print("The signature is not authentic.")
    except FileNotFoundError:
        print("No key found for " + name)
        print("Please generate a key first")

if __name__ == '__main__':
    name = input("Enter your name: ")
    main(name)