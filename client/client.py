import socket
import threading
from event_handler import receive_message, downloaded_message

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostname = socket.gethostname()
	ip_addr = socket.gethostbyname(hostname)
	user = None
	port = 10000
	success_code = None
	dm_person = None

	def send_msg(self, msg):
		self.sock.send(bytes(msg, 'utf-8'))

	def sign_in(self, values):	# Send message to Server
		values.update(TASK = "Sign In")
		msg = "{}".format(values)
		self.send_msg(msg)

	def sign_up(self, values):
		values.update(TASK = "Sign Up")
		msg = "{}".format(values)
		self.send_msg(msg)

	def send_friend_request(self, values):
		values.update(CURR_USER = self.user)
		values.update(TASK = "Send Friend Request")
		msg = "{}".format(values)
		self.send_msg(msg)
	
	def respond_friend_request(self, values):
		values.update(CURR_USER = self.user)
		values.update(TASK = "Respond Friend Request")
		msg = "{}".format(values)
		self.send_msg(msg)

	def message_person(self, values):
		values.update(DM_PERSON = self.dm_person)
		values.update(USERNAME = (self.user)["username"])
		values.update(TASK = "Message User")
		msg = "{}".format(values)
		self.send_msg(msg)

	def receive_data_loop(self):
		while True:	# Main thread is on loop continually waiting to receive data
			data = self.sock.recv(4096)	# Receive data from server

			if not data:
				break

			data = data.decode('utf-8')
			try:

				values = eval(data)
				task = values["TASK"]
				values.pop("TASK")
				if task == "Message":
					details = values["Details"]
					receive_message(details)
				elif task == "Sign In":
					details = values["Details"]
					if details != "Error":
						details = downloaded_message(details)
						self.user = details
					else:
						self.user = False
				elif task == "Sign Up":
					details = values["Details"]
					if details != "Error":
						self.user = details
					else:
						self.user = False
				elif task == "Send Friend Request":
					self.user = values["CURR_USER"]
					self.success_code = values["-SUCCESS_CODE-"]
				elif task == "Respond Friend Request":
					self.user = values["CURR_USER"]
					self.success_code = values["-SUCCESS_CODE-"]
			except ValueError:
				pass

	def __init__(self):
		self.sock.connect((self.ip_addr, 10000))	# Connect to server with client's ip addr and port
		print("{} has connected to server.".format(self.ip_addr))

		receive_thread = threading.Thread(target=self.receive_data_loop) # Separate thread is needed to receive from server
		receive_thread.daemon = True # Will close thread when we exit program
		receive_thread.start()		# Start thread

	def set_user(self, user):
		self.user = user

	def reset_success_code(self):
		self.success_code = None

	def get_user(self):
		return self.user

	def get_success_code(self):
		return self.success_code

	def set_dm_person(self, dm_person):
		self.dm_person = dm_person

	def get_dm_person(self):
		return self.dm_person