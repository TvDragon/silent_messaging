import socket
import threading
import json

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostname = socket.gethostname()
	ip_addr = socket.gethostbyname(hostname)
	user = None
	port = 10000	

	def sign_in(self, values):	# Send message to Server
		msg = "Sign In::{}".format(values)
		self.sock.send(bytes(msg, 'utf-8'))

	def receive_data_loop(self):
		while True:	# Main thread is on loop continually waiting to receive data
			data = self.sock.recv(1024)	# Receive data from server

			if not data:
				break

			data = data.decode('utf-8')
			try:
				task, details = data.split("::")

				if task == "Sign In":
					values = eval(details)
					self.user = values
				else:
					self.user = False
			except ValueError:
				pass

	def __init__(self):
		self.sock.connect((self.ip_addr, 10000))	# Connect to server with client's ip addr and port
		print("{} has connected to server.".format(self.ip_addr))
		# send_thread = threading.Thread(target=self.send_msg)	# Separate thread is needed to send to server
		# send_thread.daemon = True	# Will close thread when we exit program
		# send_thread.start()			# Start thread

		receive_thread = threading.Thread(target=self.receive_data_loop)
		receive_thread.daemon = True
		receive_thread.start()

	def set_user(self, user):
		self.user = user

	def get_user(self):
		return self.user
		

if __name__ == "__main__":
	client = Client()