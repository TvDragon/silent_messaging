import json
from os import remove
from os.path import exists
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from threading import Lock

lock = Lock()

def write_key_pair(values, private_key, public_key):
	lock.acquire()
	fd = open("{}_private_key.pem".format(values["-USERNAME-"]), "wb")
	fd.write(private_key)
	fd.close()

	fd = open("{}_public_key.pem".format(values["-USERNAME-"]), "wb")
	fd.write(public_key)
	fd.close()
	lock.release()

def generate_key_pair(values):
	##########################GENERATE CERTIFICATE PAIR########################

	new_key = RSA.generate(2048)

	private_key = new_key.exportKey("PEM")
	public_key = new_key.publickey().exportKey("PEM")

	values.update(PUBLIC_KEY = public_key)

	return values, private_key, public_key

def create_msg_file(user):
	lock.acquire()
	filename = "{}.json".format(user["username"])
	if not exists(filename):
		contents = {
			"messages": []
		}
		f = open(filename, "w")
		contents = json.dumps(contents, indent=4)
		f.write(contents)
		f.close()
	lock.release()

def get_messages(user, friend):
	lock.acquire()
	filename = "{}.json".format(user["username"])
	f = open(filename, "r")
	contents = json.load(f)
	f.close()
	lock.release()

	messages = contents["messages"]

	for message in messages:
		try:
			if message["username"] == friend["username"]:
				return message
		except TypeError:
			if message["username"] == friend:
				return message

	return None

def write_message(message, username, dm_person, writer):
	filename = "{}.json".format(username)
	lock.acquire()
	f = open(filename, "r")
	contents = json.load(f)
	f.close()
	
	messages = contents["messages"]
	found_user = False
	
	for block in messages:
		try:
			if block["username"] == dm_person["username"]:
				responses = block["messages"]
				message = {"{}".format(writer): "{}".format(message)}
				responses.append(message)
				found_user = True
				break
		except TypeError:
			if block["username"] == dm_person:
				responses = block["messages"]
				message = {"{}".format(writer): "{}".format(message)}
				responses.append(message)
				found_user = True
				break
	
	if not found_user:
		response = {"{}".format(writer): "{}".format(message)}
		block = {}
		try:
			block = {"username": "{}".format(dm_person["username"]), "messages": [response]}
		except TypeError:
			block = {"username": "{}".format(dm_person), "messages": [response]}
		messages.append(block)

	contents = {"messages": messages}
	contents = json.dumps(contents, indent=4)
	f = open(filename, "w")
	f.write(contents)
	f.close()
	lock.release()

def get_private_key(username):
	filename = "{}_private_key.pem".format(username)
	if exists(filename):
		return open(filename).read()

	return None