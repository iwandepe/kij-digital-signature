import site
import sys
from PDFNetPython3.PDFNetPython import *
from shutil import copyfile

LicenseKey = 'demo:1667292716681:7aafb59103000000002f917f8e864d0a37fac83bab71640b9b9b4baec1'

def VerifySimple(in_docpath, in_public_key_file_path):
	doc = PDFDoc(in_docpath)
	print("==========")
	opts = VerificationOptions(VerificationOptions.e_compatibility_and_archiving)

	# Add trust root to store of trusted certificates contained in VerificationOptions.
	opts.AddTrustedCertificate(in_public_key_file_path, VerificationOptions.e_default_trust | VerificationOptions.e_certification_trust)

	result = doc.VerifySignedDigitalSignatures(opts)
		
	if result is PDFDoc.e_unsigned:
		print("Dokumen tidak memiliki signature")
		return False
	elif result is PDFDoc.e_failure:
		print("Gagal memvalidasi signature.")
		return False
	elif result is PDFDoc.e_untrusted:
		print("Signature salah")
		return False
	elif result is PDFDoc.e_verified:
		print("Dokumen verified.")
		return True
	else:
		print("Something went wrong")
		assert False, "Something went wrong"

def main():
	PDFNet.Initialize(LicenseKey)
	
	result = True
	base_path = ''
	input_path = base_path + 'in/'
	output_path = base_path + 'out/'
	
	try:
		if not VerifySimple(output_path + 'file_signed.pdf', output_path + 'certificate.cer'):
			result = False
	except Exception as e:
		print(e.args)
		result = False

	if not result:
		print("VERIFIKASI GAGAL\n==========")
		return

	PDFNet.Terminate()
	print("VERIFIKASI SELESAI\n==========")

if __name__ == '__main__':
	main()