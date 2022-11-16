import socket
import threading
import sys

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def send_msg(self):	# Send message to Server
		while True:
			self.sock.send(bytes(input(""), 'utf-8'))

	def __init__(self, address):
		self.sock.connect((address, 10000))	# Connect to server with client's ip addr and port

		thread = threading.Thread(target=self.send_msg)	# Separate thread is needed to send to server
		thread.daemon = True	# Will close thread when we exit program
		thread.start()			# Start thread

		while True:	# Main thread is on loop continually waiting to receive data
			data = self.sock.recv(1024)	# Receive data from server

			if not data:
				break
			print("Message from Server: {}".format(str(data, 'utf-8')))

if __name__ == "__main__":
	if len(sys.argv) > 1:
		client = Client(sys.argv[1])
	else:
		print("Need to parse in the ip address you will be connecting from as a command line argument.")