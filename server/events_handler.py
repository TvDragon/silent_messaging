import PySimpleGUI as sg
from hashlib import sha256
from datetime import datetime

from database import write_to_db, get_users, update_db, write_log_connection

def log_connection_to_server(addr):
	msg = "Time: {} - {}:{} connected".format(datetime.now(),
												str(addr[0]), str(addr[1]))
	write_log_connection(msg)

def log_disconnection_to_server(addr):
	msg = "Time: {} - {}:{} disconnected".format(datetime.now(),
													str(addr[0]), str(addr[1]))
	write_log_connection(msg)

def add_user(values):
	hashed_password = sha256(values["-PASSWORD-"].encode('utf-8')).hexdigest()
	# new_user = User(values["-FULL_NAME-"], values["-USERNAME-"],
	# 				values["-EMAIL-"], hashed_password)
	new_user = {
		"name": values["-FULL_NAME-"],
		"username": values["-USERNAME-"],
		"hashed password": hashed_password,
		"email": values["-EMAIL-"],
		"friends": [],
		"recent_dms": [],
		"pending": []
	}
	username_taken = write_to_db(new_user)

	return username_taken, new_user

def find_user(values):
	users = get_users()
	hashed_password = sha256(values["-PASSWORD-"].encode('utf-8')).hexdigest()

	for user in users:
		if values["-USERNAME-"] == user["username"] and \
			hashed_password == user["hashed password"]:
			return True, user

	return False, None

def add_friend(values):
	username = values["-USERNAME_ADD-"]
	curr_user = values["CURR_USER"]
	if curr_user["username"] == username:
		return 1, curr_user

	users = get_users()

	for user in users:
		if user["username"] == username:
			friends_ls = curr_user["friends"]
			pending_ls = curr_user["pending"]
			for friend in friends_ls:
				if friend == username:
					return 2, curr_user	# Friend already added

			for waiting_user in pending_ls:
				if waiting_user["username"] == username and \
					waiting_user["waiting"] == "waiting_other_user":
					return 3, curr_user	# Already waiting on user to accept request

			block = {"username": "{}".format(username), 
					"waiting": "waiting_other_user"}
			pending_ls.append(block)
			curr_user["pending"] = pending_ls
			update_db(curr_user)
			
			pending_ls = user["pending"]
			block = {"username": "{}".format(curr_user["username"]),
					"waiting": "waiting_on_you"}
			pending_ls.append(block)
			user["pending"] = pending_ls
			update_db(user)
			return 0, curr_user

	return 4, curr_user	# Username doesn't exist

def perform_task(msg):

	msg = msg.decode('utf8')

	try:
		task, details = msg.split("::")
		
		if task == "Sign In":
			values = eval(details)
			found_user, user = find_user(values)
			if found_user:
				return 100, user
			return 1, None
		elif task == "Sign Up":
			values = eval(details)
			username_taken, new_user = add_user(values)
			if not username_taken:
				return 100, new_user
			return 1, False
		elif task == "Add Friend":
			pass
		elif task == "Send Friend Request":
			values = eval(details)
			success, user = add_friend(values)
			return success, user
		elif task == "Forgot Password":
			pass
	except ValueError:
		print("Perform Task Error")