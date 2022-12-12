import json
from os import remove
from os.path import exists
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def write_key_pair(values, private_key, public_key):
	fd = open("{}_private_key.pem".format(values["-USERNAME-"]), "wb")
	fd.write(private_key)
	fd.close()

	fd = open("{}_public_key.pem".format(values["-USERNAME-"]), "wb")
	fd.write(public_key)
	fd.close()

def generate_key_pair(values):
	##########################GENERATE CERTIFICATE PAIR########################

	new_key = RSA.generate(2048)

	private_key = new_key.exportKey("PEM")
	public_key = new_key.publickey().exportKey("PEM")

	values.update(PUBLIC_KEY = public_key)

	return values, private_key, public_key

def create_msg_file(user):
	
	filename = "{}.json".format(user["username"])
	if not exists(filename):
		contents = {
			"messages": []
		}
		f = open(filename, "w")
		contents = json.dumps(contents, indent=4)
		f.write(contents)
		f.close()