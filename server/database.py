import json
from datetime import datetime
from threading import Lock
from os.path import exists
from os import getcwd
from log_queries import write_to_log

path = getcwd()
users_filename = "{}/users.json".format(path)
messages_filename = "{}/messages.json".format(path)
lock_users = Lock()
lock_messages = Lock()

def create_messages_file():
	lock_messages.acquire()
	if not exists(messages_filename):
		f = open(messages_filename, "w")
		messages = []
		messages = json.dumps(messages, indent=4)
		f.write(messages)
		f.close()

	lock_messages.release()

def get_users():
	lock_users.acquire()				# Lock file for no modifications can be made when reading file
	if exists(users_filename):
		f = open(users_filename, "r")
		users = json.load(f)
		f.close()
	else:
		users = []

	lock_users.release()				# Release lock_users so other threads can access file
	return users

def update_db(curr_user):
	users = get_users()

	i = 0
	while (i < len(users)):
		if users[i]['username'] == curr_user['username']:
			users[i] = curr_user
		i += 1

	lock_users.acquire()				# Lock file for writing so multiple threads cannot write to same file
	f = open(users_filename, "w")
	users = json.dumps(users, indent=4)
	f.write(users)
	f.close()
	current_time = datetime.now()
	text = "Time: {} - Updated User Details: {}".format(current_time,
														curr_user["username"])
	write_to_log(text)
	lock_users.release()				# Release lock_users so other threads can write to file
	

def write_to_db(new_user):
	users = get_users()

	username_taken = False
	for user in users:
		if user['username'] == new_user['username']:
			username_taken = True
			break

	if not username_taken:
		users.append(new_user)
		lock_users.acquire()				# Lock file for writing so multiple threads cannot write to same file
		f = open(users_filename, "w")
		users = json.dumps(users, indent=4)
		f.write(users)
		f.close()
		current_time = datetime.now()
		text = "Time: {} - New User Added: {}".format(current_time,
														new_user["username"])
		write_to_log(text)
		lock_users.release()				# Release lock_users so other threads can write to file

	return username_taken

def get_messages(receiver):
	lock_messages.acquire()
	f = open(messages_filename, "r")
	all_messages = json.load(f)
	f.close()
	messages = None

	i = 0
	while i < len(all_messages):
		if all_messages[i]["username"] == receiver:
			messages = all_messages[i]["messages"]
			del all_messages[i]
			break

		i += 1

	f = open(messages_filename, "w")
	all_messages = json.dumps(all_messages, indent=4)
	f.write(all_messages)
	f.close()

	lock_messages.release()
	return messages

def write_messages(message, sender, receiver):
	lock_messages.acquire()

	f = open(messages_filename, "r")
	all_messages = json.load(f)
	f.close()
	found_user = False

	for block in all_messages:
		if block["username"] == receiver:
			messages = block["messages"]
			for msg in messages:
				if msg["sender"] == sender:
					msgs = msg["messages"]
					msgs.append(message)
					msg["messages"] = msgs
			block["messages"] = messages
			found_user = True
			break

	if not found_user:
		block = {
			"username": "{}".format(receiver),
			"messages": [{
				"sender": "{}".format(sender),
				"messages": [message]
			}]
		}
		all_messages.append(block)

	f = open(messages_filename, "w")
	all_messages = json.dumps(all_messages, indent=4)
	f.write(all_messages)
	f.close()
	lock_messages.release()

def write_log_connection(msg):
	lock_users.acquire()
	write_to_log(msg)
	lock_users.release()