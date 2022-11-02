""" TABLE OF CONTENTS
- generate a pair of key
  - store the keys in separate files
- create signature
  - create signature based on a pdf file
- create certif
  - create identity of ISSUER
- embed certif
  - save new certified file
- extract / clear certif
- signature validation
"""

import OpenSSL
import os
import time
import argparse
from PDFNetPython3.PDFNetPython import *
from typing import Tuple
from shutil import copyfile

#===== start:CONFIG_FIELD =====
RELATIVE_PATH = '' # '/home/allam/dev-project/kij-digital-signature/' # '/content/drive/MyDrive/kij/' # sesuaikan sendiri
INPUT_PATH = 'in/' # WARNING!!! yang boleh akses input path adalah fungsi copyInputFiles() lainnya gunakan OUTPUT_PATH
OUTPUT_PATH = 'out/'
KEY_PDFNET = 'demo:1667292716681:7aafb59103000000002f917f8e864d0a37fac83bab71640b9b9b4baec1'

ISSUER_NAME = "ALLAM TAJU SAROF"
ISSUER_COUNTRY = "id"
ISSUER_PROVINCE = "Jawa Timur"
ISSUER_CITY = "Surabaya"
ISSUER_EMAIL = "allamtaju4@gmail.com"
ISSUER_ORGANIZATION = "KIJ"
ISSUER_ORGANIZATION_UNIT = "KIJ Digital Signature"

CERTIFICATE_PASSWORD = 'password'
SIGN_ID = 'ATS'
SIGN_COORDINATE_X = 500 # 0 start from left
SIGN_COORDINATE_Y = 50 # 0 start from bottom
SIGN_WIDTH = 100
SIGN_HEIGHT = 50
#===== end:CONFIG_FIELD =====

""" FUNCTIONS TO GENERATE """
# this function modified from https://www.thepythoncode.com/article/sign-pdf-files-in-python
def createKeyPair(type, bits):
    """
    Create a public/private key pair
    Arguments: Type - OpenSSL.crypto.TYPE_RSA or OpenSSL.crypto.TYPE_DSA
               bits - Number of bits to use in the key (1024 or 2048 or 4096)
    Returns: The public/private key pair in a PKey object
    """
    pkey = OpenSSL.crypto.PKey()
    pkey.generate_key(type, bits)
    return pkey

def create_self_signed_cert(pKey):
    """Create a self signed certificate. This certificate will not require to be signed by a Certificate Authority."""
    # Create a self signed certificate
    cert = OpenSSL.crypto.X509()
    # Common Name (e.g. server FQDN or Your Name)
    cert.get_subject().commonName  = ISSUER_NAME
    cert.get_subject().countryName = ISSUER_COUNTRY
    cert.get_subject().stateOrProvinceName = ISSUER_PROVINCE
    cert.get_subject().localityName = ISSUER_CITY
    cert.get_subject().emailAddress = ISSUER_EMAIL
    cert.get_subject().organizationName = ISSUER_ORGANIZATION
    cert.get_subject().organizationalUnitName = ISSUER_ORGANIZATION_UNIT
    # Serial Number
    cert.set_serial_number(int(time.time() * 10))
    # Not Before
    cert.gmtime_adj_notBefore(0)  # Not before
    # Not After (Expire after 10 years)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    # Identify issue
    cert.set_issuer((cert.get_subject()))
    cert.set_pubkey(pKey)
    cert.sign(pKey, 'sha256') # or cert.sign(pKey, 'md5')
    return cert

""" FUNCTIONS TO MANAGE FILES """
def copyInputFiles():
    """ copy input (only files not folders) from input folder to output folder """
    for foldername, dirs, filenames in os.walk(RELATIVE_PATH + INPUT_PATH):
        for filename in filenames:
            copyfile(RELATIVE_PATH + INPUT_PATH + filename, RELATIVE_PATH + OUTPUT_PATH + filename)
            
    return

def storePrivateKey(pkey):
    with open(RELATIVE_PATH + OUTPUT_PATH + 'private_key.pem', 'wb') as pk_file:
        pk_str = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, pkey)
        pk_file.write(pk_str)
        return pk_str

def storePublicKey(pkey):
    with open(RELATIVE_PATH + OUTPUT_PATH + 'public_key.pem', 'wb') as pub_key_file:
        pub_key_str = OpenSSL.crypto.dump_publickey(
            OpenSSL.crypto.FILETYPE_PEM, pkey)
        #print("Public key = ",pub_key_str)
        pub_key_file.write(pub_key_str)
        return pub_key_str

def storeCertificate(cert):
    with open(RELATIVE_PATH + OUTPUT_PATH + 'certificate.cer', 'wb') as cer_file:
        cer_str = OpenSSL.crypto.dump_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        cer_file.write(cer_str)
        return cer_str

def storeCertificatePKCS12(cert, pkey):
    with open(RELATIVE_PATH + OUTPUT_PATH + 'certificate.pfx', 'wb') as p12_file:
        p12 = OpenSSL.crypto.PKCS12()
        p12.set_certificate(cert)
        p12.set_privatekey(pkey)
        p12_str = p12.export(CERTIFICATE_PASSWORD)
        p12_file.write(p12_str)
        return p12_str

""" FUNCTIONS TO PRINT CONSOLE LOG"""
def summaryPrint(summary):
    print("################# Summary ##################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("############################################################################\n")
    return


""" FUNCTIONS DRIVERS """
def certificateGenerator():
    """Generate the certificate"""
    summary = {}
    summary['OpenSSL Version'] = OpenSSL.__version__
    # Generating a Private Key...
    key = createKeyPair(OpenSSL.crypto.TYPE_RSA, 1024)

    # PEM encoded, create private key and public key in separate files
    summary['Private Key'] = storePrivateKey(key)
    summary['Public Key'] = storePublicKey(key)

    # Generating a Certificate...
    cert = create_self_signed_cert(pKey=key)
    summary['Self Signed Certificate'] = storeCertificate(cert)
    
    # Take a private key and a certificate and combine them into a PKCS12 file.
    # Generating a container file of the private key and the certificate...
    summary['PKCS12 Certificate'] = storeCertificatePKCS12(cert, key)
    # You may convert a PKSC12 file (.pfx) to a PEM format
    # Done - Generating a container file of the private key and the certificate...
    # To Display A Summary
    summaryPrint(summary)
    return True

def signFile(input_file: str, signatureID: str, x_coordinate: int, 
            y_coordinate: int, pages: Tuple = None, output_file: str = None
              ):
    """Sign a PDF file"""
    # An output file is automatically generated with the word signed added at its end
    if not output_file:
        output_file = (os.path.splitext(input_file)[0]) + "_signed.pdf"
    # Initialize the library
    PDFNet.Initialize(KEY_PDFNET)
    doc = PDFDoc(input_file)
    # Create a signature field
    sigField = SignatureWidget.Create(
        doc, 
        Rect(
            x_coordinate, 
            y_coordinate, 
            x_coordinate + SIGN_WIDTH, 
            y_coordinate + SIGN_HEIGHT
        ), 
        signatureID
    )
    # Iterate throughout document pages
    for page in range(1, (doc.GetPageCount() + 1)):
        # If required for specific pages
        if pages:
            if str(page) not in pages:
                continue
        pg = doc.GetPage(page)
        # Create a signature text field and push it on the page
        pg.AnnotPushBack(sigField)
    # Signature image
    sign_filename = RELATIVE_PATH + OUTPUT_PATH + "signature.png"
    # Self signed certificate
    pk_filename = RELATIVE_PATH + OUTPUT_PATH + "certificate.pfx"
    # Retrieve the signature field.
    approval_field = doc.GetField(signatureID)
    approval_signature_digsig_field = DigitalSignatureField(approval_field)
    # Add appearance to the signature field.
    img = Image.Create(doc.GetSDFDoc(), sign_filename)
    found_approval_signature_widget = SignatureWidget(
        approval_field.GetSDFObj())
    found_approval_signature_widget.CreateSignatureAppearance(img)
    # Prepare the signature and signature handler for signing.
    approval_signature_digsig_field.SignOnNextSave(pk_filename, CERTIFICATE_PASSWORD)
    # The signing will be done during the following incremental save operation.
    doc.Save(output_file, SDFDoc.e_incremental)
    # Develop a Process Summary
    summary = {
        "Input File": input_file, "Signature ID": signatureID, 
        "Output File": output_file, "Signature File": sign_filename, 
        "Certificate File": pk_filename
    }
    # Printing Summary
    summaryPrint(summary)
    return True

def generateThenSign():
    copyInputFiles()
    certificateGenerator()

    args = {
        'input_path': RELATIVE_PATH + OUTPUT_PATH + "file.pdf",
        'signatureID': SIGN_ID, 
        'pages': None, 
        'x_coordinate': SIGN_COORDINATE_X, 
        'y_coordinate': SIGN_COORDINATE_Y, 
        'output_file': None
    }
    signFile(
        input_file=args['input_path'], signatureID=args['signatureID'],
        x_coordinate=int(args['x_coordinate']), y_coordinate=int(args['y_coordinate']), 
        pages=args['pages'], output_file=args['output_file']
    )

generateThenSign()