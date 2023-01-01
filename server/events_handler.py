from hashlib import sha256
from datetime import datetime
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import chardet

from database import write_to_db, get_users, update_db, write_log_connection, \
	create_messages_file, write_messages, get_messages, get_user_key

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
	public_key = values["PUBLIC_KEY"].decode("utf-8")

	new_user = {
		"username": values["-USERNAME-"],
		"hashed password": hashed_password,
		"email": values["-EMAIL-"],
		"public key": public_key,	# Will need to convert this back to bytes when encrypting messages
		"public_ip": "",
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

def respond_friend_request(values):
	username = values["username"]
	curr_user = values["CURR_USER"]
	response = values["-ACCEPT-"]

	users = get_users()

	for user in users:
		if user["username"] == username:
			friends_ls = curr_user["friends"]
			pending_ls = curr_user["pending"]

			if response == "YES":
				pub_key = get_user_key(username)
				friend = {"username": username, "public key": pub_key}
				friends_ls.append(friend)
				curr_user["friends"] = friends_ls
				update_db(curr_user)

				friends_ls = user["friends"]
				pub_key = get_user_key(curr_user["username"])
				friend = {"username": curr_user["username"],
							"public key": pub_key}
				friends_ls.append(friend)
				update_db(user)

			new_pending_ls = []
			for waiting_user in pending_ls:
				if waiting_user["username"] != username:
					new_pending_ls.append(waiting_user)	

			curr_user["pending"] = new_pending_ls
			update_db(curr_user)

			pending_ls = user["pending"]
			new_pending_ls = []
			for waiting_user in pending_ls:
				if waiting_user["username"] != curr_user["username"]:
					new_pending_ls.append(waiting_user)

			user["pending"] = new_pending_ls
			update_db(user)
			break

	return 500, curr_user

def send_msg_to_user(values, connections):
	dm_person = values["DM_PERSON"]

	users = get_users()

	for user in users:
		if dm_person == user["username"]:
			public_ip = user["public_ip"]

			for conn in connections:
				ip = "{}:{}".format(conn.getpeername()[0], conn.getpeername()[1])
				if ip == public_ip:
					return 200, [conn, values]

	# Receiver is not online to receive message
	return -1, None

def store_message_to_db(values):
	sender = values["USERNAME"]
	receiver = values["DM_PERSON"]
	message = values["-MESSAGE-"]
	key = get_user_key(receiver)
	key = RSA.import_key(key)
	cipher = PKCS1_OAEP.new(key)
	ciphertext = str(cipher.encrypt(message.encode("utf-8")))

	# text = ""
	# for char in ciphertext:
	# 	if char == '"':
	# 		text += "\""
	# 	text += char

	# print(text)

	write_messages(ciphertext, sender, receiver)

def perform_task(msg, addr, connections):

	msg = msg.decode('utf8')

	try:
		values = eval(msg)
		task = values["TASK"]
		values.pop("TASK")
		if task == "Message User":
			success, data = send_msg_to_user(values, connections)
			
			if success == -1:	# Write message to database temporarily until receivers logs back on to receive message
				store_message_to_db(values)

			return success, data
		elif task == "Sign In":
			found_user, user = find_user(values)
			if found_user:
				public_addr = "{}:{}".format(addr[0], addr[1])
				user.update(public_ip = public_addr)
				update_db(user)
				messages = get_messages(user["username"])
				user.update(MESSAGE = messages)
				return 100, user
			return 1, None
		elif task == "Sign Up":
			username_taken, new_user = add_user(values)
			if not username_taken:
				new_user.update(MESSAGE = None)
				return 100, new_user
			return 1, False
		elif task == "Add Friend":
			pass
		elif task == "Send Friend Request":
			success, user = add_friend(values)
			return success, user
		elif task == "Respond Friend Request":
			return respond_friend_request(values)
		elif task == "Forgot Password":
			pass
	# except ValueError:
	# 	print("Perform Task Error")
	except SyntaxError:
		print("Syntax Error Occurred")

def remove_ip_for_user(addr):
	users = get_users()
	public_addr = "{}:{}".format(addr[0], addr[1])

	for user in users:
		if user["public_ip"] == public_addr:
			user["public_ip"] = ""
			update_db(user)
			break

def open_messages():
	create_messages_file()