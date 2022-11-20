from hashlib import sha256

class User:
	def __init__(self, name, username, email, hashed_password, friends=[]):
		self.name = name
		self.username = username
		self.email = email
		self.hashed_password = hashed_password
		self.friends = friends	# Initally an empty list if not defined

	def set_name(self, name):
		self.name = name
	
	def set_username(self, username):
		self.username = username

	def set_email(self, email):
		self.email = email

	def set_password(self, password):
		self.hashed_password = sha256(password.encode('utf-8')).hexdigest()

	def add_friend(self, friend):
		if friend not in self.friends:
			self.friends.append(friend)

	def get_name(self):
		return self.name

	def get_username(self):
		return self.username

	def get_email(self):
		return self.email

	def get_hashed_password(self):
		return self.hashed_password

	def get_friends(self):
		return self.friends