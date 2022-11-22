import socket
import threading

class Client:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	hostname = socket.gethostname()
	ip_addr = socket.gethostbyname(hostname)

	def send_msg(self):	# Send message to Server
		while True:
			self.sock.send(bytes(input(""), 'utf-8'))

	def receive_data_loop(self):
		while True:	# Main thread is on loop continually waiting to receive data
			data = self.sock.recv(1024)	# Receive data from server

			if not data:
				break
			print("Message from Server: {}".format(str(data, 'utf-8')))

	def __init__(self):
		self.sock.connect((self.ip_addr, 10000))	# Connect to server with client's ip addr and port
		print(self.ip_addr)
		send_thread = threading.Thread(target=self.send_msg)	# Separate thread is needed to send to server
		send_thread.daemon = True	# Will close thread when we exit program
		send_thread.start()			# Start thread

		receive_thread = threading.Thread(target=self.receive_data_loop)
		receive_thread.daemon = True
		receive_thread.start()
		

if __name__ == "__main__":
	client = Client()