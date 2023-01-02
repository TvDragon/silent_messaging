import json
from os.path import exists
from threading import Lock

lock = Lock()

def create_msg_file(username):
	lock.acquire()
	filename = "{}.json".format(username)
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
		if block["username"] == dm_person:
			responses = block["messages"]
			message = {"{}".format(writer): "{}".format(message)}
			responses.append(message)
			found_user = True
			break
	
	if not found_user:
		response = {"{}".format(writer): "{}".format(message)}
		block = {"username": "{}".format(dm_person), "messages": [response]}
		messages.append(block)

	contents = {"messages": messages}
	contents = json.dumps(contents, indent=4)
	f = open(filename, "w")
	f.write(contents)
	f.close()
	lock.release()