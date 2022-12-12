import json
from datetime import datetime
from threading import Lock
from os.path import exists
from os import getcwd
from log_queries import write_to_log

path = getcwd()
users_filename = "{}/users.json".format(path)
lock = Lock()

def write_messages():
	lock.acquire()
	messages_filename = "{}/messages".format(path)
	if exists(messages_filename):
		pass
	else:
		f = open(messages_filename, "w")
		f.close()

	lock.release()

def get_users():
	lock.acquire()				# Lock file for no modifications can be made when reading file
	if exists(users_filename):
		f = open(users_filename, "r")
		users = json.load(f)
		f.close()
	else:
		users = []

	lock.release()				# Release lock so other threads can access file
	return users

def update_db(curr_user):
	users = get_users()

	i = 0
	while (i < len(users)):
		if users[i]['username'] == curr_user['username']:
			users[i] = curr_user
		i += 1

	lock.acquire()				# Lock file for writing so multiple threads cannot write to same file
	f = open(users_filename, "w")
	users = json.dumps(users, indent=4)
	f.write(users)
	f.close()
	current_time = datetime.now()
	text = "Time: {} - Updated User Details: {}".format(current_time,
														curr_user["username"])
	write_to_log(text)
	lock.release()				# Release lock so other threads can write to file
	

def write_to_db(new_user):
	users = get_users()

	username_taken = False
	for user in users:
		if user['username'] == new_user['username']:
			username_taken = True
			break

	if not username_taken:
		users.append(new_user)
		lock.acquire()				# Lock file for writing so multiple threads cannot write to same file
		f = open(users_filename, "w")
		users = json.dumps(users, indent=4)
		f.write(users)
		f.close()
		current_time = datetime.now()
		text = "Time: {} - New User Added: {}".format(current_time,
														new_user["username"])
		write_to_log(text)
		lock.release()				# Release lock so other threads can write to file

	return username_taken

def write_log_connection(msg):
	lock.acquire()
	write_to_log(msg)
	lock.release()