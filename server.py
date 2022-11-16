import socket
import threading
import sys

class Server:

	# Create socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# First Param - Send information using IP version 4 instead of IP version 6. Second Param - TCP connection
	connections = []

	def __init__(self):
		# Bind connection to address and port
		self.sock.bind(('0.0.0.0', 10000)) # 0.0.0.0 is used as it will make our server available over any IP address that's configured on the server

		# Listen
		self.sock.listen(1) # Pass in a variable of the number of pending connections you want to allow


	def handler(self, conn, addr):	# Accepts arguments
		# Receive data from connection
		while True:
			data = conn.recv(1024)	# Max amount of data we can receive is 1024 bytes
			# recv() is a blocking function so loop won't run until we actually receive some data
			# Send data back to users
			for connection in self.connections:
				if conn != connection:
					connection.send(bytes(data))	# Can only send back raw bytes
			if not data:
				print(str(addr[0]) + ":" + str(addr[1]), "disconnected")
				self.connections.remove(conn)	# Remove connection from list of connections
				conn.close() # Close connection
				break

	def run(self):
		# Handle connections
		while True:

			conn, addr = self.sock.accept()	# Returns connections and client address
			conn_thread = threading.Thread(target=self.handler, args=(conn, addr))	# Name of function to run
			conn_thread.daemon = True	# Setting to true means program can exit regardless of if there's any threads still running
			conn_thread.start()			# Start the thread
			self.connections.append(conn)
			# print(self.connections)
			print(str(addr[0]) + ":" + str(addr[1]), "connected")

if __name__ == "__main__":
	server = Server()
	server.run()