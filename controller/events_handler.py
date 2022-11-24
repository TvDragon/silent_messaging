import PySimpleGUI as sg
import sys
from os import getcwd
from hashlib import sha256

path = getcwd()
sys.path.insert(0, "{}/model/".format(path))
sys.path.insert(0, "{}/".format(path))

from user import User
from database import write_to_db, get_users

def add_user(values):
	hashed_password = sha256(values["-PASSWORD-"].encode('utf-8')).hexdigest()
	new_user = User(values["-FULL_NAME-"], values["-USERNAME-"],
					values["-EMAIL-"], hashed_password)
	new_user = {
		"name": values["-FULL_NAME-"],
		"username": values["-USERNAME-"],
		"hashed password": hashed_password,
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