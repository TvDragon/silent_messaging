import PySimpleGUI as sg

WIDTH = 512
HEIGHT = 240
MESSAGE_SCREEN_WIDTH = 1280
MESSAGE_SCREEN_HEIGHT = 960

def sign_up_scene():
	return [[sg.Text("Sign Up", font=("Arial", 20))],
			[sg.Text(key="-OUTPUT-", text_color="yellow")],
			[sg.Text("Username"), sg.Input(key="-USERNAME-", size=(30, 1),
				text_color="white")],
			[sg.Text("Email\t"), sg.Input(key="-EMAIL-", size=(30, 1),
				text_color="white",)],
			[sg.Text("Password"), sg.Input(key="-PASSWORD-", size=(30, 1),
				password_char="*", text_color="white")],
			[sg.Button("Sign Up")],
			[sg.Text("Already Have an Account?"),
			sg.Text("Sign In", key="-SIGN_IN-", enable_events=True,
					text_color="grey")]]

def login_scene():
	return [[sg.Text("Sign In", font=("Arial", 20))],
			[sg.Text(key="-OUTPUT-", text_color="yellow")],
			[sg.Text("Username"), sg.Input(key="-USERNAME-", size=(30, 1),
				text_color="white")],
			[sg.Text("Password"), sg.Input(key="-PASSWORD-", size=(30, 1),
				password_char="*", text_color="white")],
			[sg.Button("Sign In")],
			[sg.Text("Forgot Password?", key="-FORGOT_PASSWORD-",
				enable_events=True, text_color="grey")],
			[sg.Text("Don't have an account?"),
			sg.Text("Sign Up", key="-SIGN_UP-", enable_events=True,
					text_color="grey")]]

def recent_messages(user):
	recent_dms = [[sg.Text("Friends", key="-FRIENDS-", enable_events=True,
							text_color="grey", font=("Arial", 20))],
						[sg.Text("Direct messages", font=("Arial", 16))]]
	
	friends = user["recent_dms"]

	for friend in friends:
		recent_dms.append([sg.Text("{}".format(list(friend.keys())[0]),
							font=("Arial", 12))])

	return recent_dms

def message_scene(user, dm_person):
	
	recent_dms = recent_messages(user)

	message = [[sg.Text("{}".format(dm_person), font=("Arial", 20))],
				[sg.Text("Message....", font=("Arial", 14))],
				[sg.Text("Message 2.....", font=("Arial", 14))],
				[sg.Text("Message 3.....", font=("Arial", 14))]]

	# Find dm_person and loop through messages with them

	return [[sg.Column(recent_dms, size=(200, MESSAGE_SCREEN_HEIGHT)),
			sg.Column(message, scrollable=True, vertical_scroll_only=True,
						size=(MESSAGE_SCREEN_WIDTH - 200,
										MESSAGE_SCREEN_HEIGHT))]]

def add_friend_scene(user):
	
	recent_dms = recent_messages(user)

	find_user = [[sg.Text("Add Friend", font=("Arial", 20))],
				[sg.Text("Enter a username:", font=("Arial", 16)),
				sg.Input(key="-USERNAME_ADD-", size=(30, 1),
				text_color="white"),
				sg.Button("Send Friend Request")],
				[sg.Text("", key="-FRIEND_ADDED_SUCCESS-")]
		]

	return [[sg.Column(recent_dms, size=(200, MESSAGE_SCREEN_HEIGHT)),
			sg.Column(find_user, size=(MESSAGE_SCREEN_WIDTH - 200,
										MESSAGE_SCREEN_HEIGHT))]]

def pending_friends_scene(user):
	
	recent_dms = recent_messages(user)

	pending_friends_ls = [[sg.Text("Friends", font=("Arial", 20)),
					sg.Text("All", key="-ALL_FRIENDS-", enable_events=True,
					font=("Arial", 16), text_color="grey"),
					sg.Text("Pending", key="-PENDING-", enable_events=True,
					font=("Arial", 16), text_color="grey"),
					sg.Button("Add Friend")
			]]

	pending_friends = user["pending"]

	for pending in pending_friends:
		username = pending["username"]
		waiting = pending["waiting"]
		if waiting == "waiting_other_user":
			pending_friends_ls.append([sg.Text("{}".format(username),
											font=("Arial", 14)),
										sg.Text("X",
											key="-X_{}-".format(username),
											enable_events=True,
											font=("Arial", 14),
											text_color="red")])	# Option to cancel friend request
		else:
			pending_friends_ls.append([sg.Text("{}".format(username),
											font=("Arial", 14)),
										sg.Text("Y",
											key="-Y_{}-".format(username),
											enable_events=True,
											font=("Arial", 14),
											text_color="green"),	# Option to accept friend request
										sg.Text("X",
											key="-X_{}-".format(username),
											enable_events=True,
											font=("Arial", 14),
											text_color="red")])	# Option to deny friend request

	return [[sg.Column(recent_dms, size=(200, MESSAGE_SCREEN_WIDTH)),
			sg.Column(pending_friends_ls, size=(MESSAGE_SCREEN_WIDTH - 200,
												MESSAGE_SCREEN_HEIGHT))]]

def friends_list(user):

	recent_dms = recent_messages(user)

	friends_ls = [[sg.Text("Friends", font=("Arial", 20)),
					sg.Text("All", key="-ALL_FRIENDS-", enable_events=True,
					font=("Arial", 16), text_color="grey"),
					sg.Text("Pending", key="-PENDING-", enable_events=True,
					font=("Arial", 16), text_color="grey"),
					sg.Button("Add Friend")
			]]

	friends = user["friends"]

	for friend in friends:
		friends_ls.append([sg.Text("{}".format(friend),
							key="-{}-".format(friend),
							enable_events=True, font=("Arial", 14),
							text_color="grey")])

	return [[sg.Column(recent_dms, size=(200, MESSAGE_SCREEN_WIDTH)),
			sg.Column(friends_ls, size=(MESSAGE_SCREEN_WIDTH - 200,
											MESSAGE_SCREEN_HEIGHT))]]