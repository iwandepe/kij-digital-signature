from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

def main():
    file_path = 'public/file.pdf'

    with open(file_path, "rb") as file:
        file_data = file.read()

    key = RSA.import_key(open('public.key').read())
    h = SHA256.new(file_data)
    verifier = pss.new(key)

    try:
        with open('public/file.pdf.sig', "rb") as signature_file:
            signature = signature_file.read()
            verifier.verify(h, signature)
            print("The signature is authentic.")
    except (ValueError, TypeError):
        print("The signature is not authentic.")

if __name__ == '__main__':
    main()