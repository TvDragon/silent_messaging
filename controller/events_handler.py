import PySimpleGUI as sg
import sys
from os import getcwd
from hashlib import sha256

path = getcwd()
sys.path.insert(0, "{}/model/".format(path))
sys.path.insert(0, "{}/".format(path))

from user import User
from database import write_to_db, get_users, update_db

def add_user(values):
	hashed_password = sha256(values["-PASSWORD-"].encode('utf-8')).hexdigest()
	# new_user = User(values["-FULL_NAME-"], values["-USERNAME-"],
	# 				values["-EMAIL-"], hashed_password)
	new_user = {
		"name": values["-FULL_NAME-"],
		"username": values["-USERNAME-"],
		"hashed password": hashed_password,
		"email": values["-EMAIL-"],
		"friends": [
		],
		"recent_dms": [

		]
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

def add_friend(curr_user, values):
	username = values["-USERNAME_ADD-"]
	if curr_user["username"] == username:
		return 1

	users = get_users()

	for user in users:
		if user["username"] == username:
			friends_ls = curr_user["friends"]
			for friend in friends_ls:
				if friend == username:
					return 2	# Friend already added

			friends_ls.append(username)
			curr_user["friends"] = friends_ls
			update_db(curr_user)
			
			friends_ls = user["friends"]
			friends_ls.append(curr_user["username"])
			user["friends"] = friends_ls
			update_db(user)			
			return 0

	return 3

def perform_task(msg):

	msg = msg.decode('utf8')

	try:
		task, details = msg.split("::")
		
		if task == "Sign In":
			values = eval(details)
			found_user, user = find_user(values)
			if found_user:
				return user
			return None
		elif task == "Sign Up":
			values = eval(details)
			username_taken, new_user = add_user(values)
			if not username_taken:
				return new_user
			return False
		elif task == "Add Friend":
			pass
		elif task == "Send Friend Request":
			pass
		elif task == "Forgot Password":
			pass
	except ValueError:
		print("Perform Task Error")