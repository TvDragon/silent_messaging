import socket
import threading

from events_handler import perform_task, log_connection_to_server, log_disconnection_to_server

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

			success, user = perform_task(data)
			msg = ""
			if user != None and success == 100:
				msg = "Sign In::{}".format(str(user))
			elif user == None:
				msg = "Sign In::Error"
			elif user == False:
				msg = "Sign Up::Error"
			elif user != None:
				values = {"-SUCCESS_CODE-": success}
				values.update(CURR_USER = user)
				msg = "Send Friend Request::{}".format(values)
			
			conn.send(bytes(msg, 'utf-8'))	# Send into back to user

			if not data:
				log_disconnection_to_server(addr)
				self.connections.remove(conn)	# Remove connection from list of connections
				conn.close() # Close connection
				break

	def run(self):
		# Handle connections
		while True:

			conn, addr = self.sock.accept()	# Returns connections and client address
			conn_thread = threading.Thread(target=self.handler, 
											args=(conn, addr))	# Name of function to run
			conn_thread.daemon = True	# Setting to true means program can exit regardless of if there's any threads still running
			conn_thread.start()			# Start the thread
			self.connections.append(conn)
			log_connection_to_server(addr)

if __name__ == "__main__":
	server = Server()
	server.run()