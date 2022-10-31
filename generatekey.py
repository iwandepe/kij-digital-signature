import os
from Crypto.PublicKey import RSA

def generate_key(name):
    try:
        os.makedirs('keys/' + name)
    except OSError as error:
        print('Replacing existing key')

    key = RSA.generate(2048)
    private_key = key.export_key()
    file_out = open('keys/' + name + '/private.pem', 'wb')
    file_out.write(private_key)

    public_key = key.publickey().export_key()
    file_out = open('keys/' + name + '/public.pem', 'wb')
    file_out.write(public_key)

if __name__ == "__main__":
    name = input("Enter your name: ")
    generate_key(name)
