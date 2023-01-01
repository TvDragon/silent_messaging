import socket
import threading

from events_handler import perform_task, log_connection_to_server, \
	log_disconnection_to_server, remove_ip_for_user, open_messages

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
			data = conn.recv(4096)	# Max amount of data we can receive is 1024 bytes
			# recv() is a blocking function so loop won't run until we actually receive some data
			
			# Error occurs here because I'm somehow disconnecting when sending message
			if not data:
				log_disconnection_to_server(addr)
				remove_ip_for_user(addr)
				self.connections.remove(conn)	# Remove connection from list of connections
				conn.close() # Close connection
				break

			# try:
			success, data = perform_task(data, addr, self.connections)
			msg = ""
			if success == 200:
				msg = "Message::{}".format(str(data[1]))
				data[0].send(bytes(msg, 'utf-8'))
				msg = ""
			elif data != None and success == 100:
				msg = "Sign In::{}".format(str(data))
			elif data == None and success == 1:
				msg = "Sign In::Error"
			elif data == False:
				msg = "Sign Up::Error"
			elif success == 500:
				values = {"-SUCCESS_CODE-": success}
				values.update(CURR_USER = data)
				msg = "Respond Friend Request::{}".format(values)
			elif data != None:
				values = {"-SUCCESS_CODE-": success}
				values.update(CURR_USER = data)
				msg = "Send Friend Request::{}".format(values)
			
			conn.send(bytes(msg, 'utf-8'))	# Send into back to user
			# except TypeError:
			# 	print("TypeError received")


	def run(self):
		open_messages()

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