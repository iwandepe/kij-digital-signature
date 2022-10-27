from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

def main():
    file_path = 'public/file.pdf'

    with open(file_path, "rb") as file:
        file_data = file.read()

    key = RSA.import_key(open('private.key').read())
    h = SHA256.new(file_data)
    signature = pss.new(key).sign(h)

    signature_path = 'public/file.pdf.sig'
    with open(signature_path, "wb") as file:
        file.write(signature)

if __name__ == '__main__':
    main()