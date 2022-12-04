import socket
import threading
import json

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostname = socket.gethostname()
	ip_addr = socket.gethostbyname(hostname)
	user = None
	port = 10000
	success_code = None

	def send_msg(self, msg):
		self.sock.send(bytes(msg, 'utf-8'))

	def sign_in(self, values):	# Send message to Server
		msg = "Sign In::{}".format(values)
		self.send_msg(msg)

	def sign_up(self, values):
		msg = "Sign Up::{}".format(values)
		self.send_msg(msg)

	def send_friend_request(self, values):
		values.update(CURR_USER = self.user)
		msg = "Send Friend Request::{}".format(values)
		self.send_msg(msg)
	
	def respond_friend_request(self, values):
		values.update(CURR_USER = self.user)
		msg = "Respond Friend Request::{}".format(values)
		self.send_msg(msg)

	def receive_data_loop(self):
		while True:	# Main thread is on loop continually waiting to receive data
			data = self.sock.recv(1024)	# Receive data from server

			if not data:
				break

			data = data.decode('utf-8')
			try:
				task, details = data.split("::")

				if task == "Sign In":
					if details != "Error":
						values = eval(details)
						self.user = values
					else:
						self.user = False
				elif task == "Sign Up":
					if details != "Error":
						values = eval(details)
						self.user = values
					else:
						self.user = False
				elif task == "Send Friend Request":
					values = eval(details)
					self.user = values["CURR_USER"]
					self.success_code = values["-SUCCESS_CODE-"]
				elif task == "Respond Friend Request":
					values = eval(details)
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
		

if __name__ == "__main__":
	client = Client()