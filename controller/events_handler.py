import PySimpleGUI as sg
import sys
from os import getcwd
from hashlib import sha256

path = getcwd()[:-4]
sys.path.insert(0, "{}model/".format(path))
sys.path.insert(0, "{}".format(path))

from user import User
from database import write_to_db

def add_user(values):
	hashed_password = sha256(values["-PASSWORD-"].encode('utf-8')).hexdigest()
	new_user = User(values["-FULL_NAME-"], values["-USERNAME-"],
					values["-EMAIL-"], hashed_password)
	new_user = {
		"name": values["-FULL_NAME-"],
		"username": values["-USERNAME-"],
		"hashed password": hashed_password,
		"friends": [
		]
	}
	username_taken = write_to_db(new_user)

	return username_taken