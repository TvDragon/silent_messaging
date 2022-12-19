from scenes import *
from client import Client
from model import create_msg_file, generate_key_pair, write_key_pair, get_messages

def handle_events(event, values, user_client, window):
	# See if user wants to quit or window was closed
	if event == sg.WINDOW_CLOSED:
		return window, 1
	elif event == "Sign In":
		user_client.sign_in(values)

		# Wait until if found user or not
		while user_client.get_user() == None:
			pass
		
		if user_client.get_user() != False:
			window.close()
			window = sg.Window("Silent Message",
								friends_list(user_client.get_user()),
								size=(MESSAGE_SCREEN_WIDTH,
										MESSAGE_SCREEN_HEIGHT))
			create_msg_file(user_client.get_user())
		else:
			window["-OUTPUT-"].update("Username or Password may be incorrect. User may not exist.")
			user_client.set_user(None)
	elif event == "-SIGN_UP-":
		window.close()
		window = sg.Window("Silent Message", sign_up_scene(),
							element_justification='c',
							size=(WIDTH, HEIGHT))
	elif event == "Sign Up":
		values, private_key, public_key = generate_key_pair(values)
		user_client.sign_up(values)

		# Wait until if found user or not
		while user_client.get_user() == None:
			pass
		
		if user_client.get_user() != False:
			write_key_pair(values, private_key, public_key)
			window.close()
			window = sg.Window("Silent Message",
								friends_list(user_client.get_user()),
								element_justification='c',
								size=(MESSAGE_SCREEN_WIDTH,
										MESSAGE_SCREEN_HEIGHT))
		else:
			window["-OUTPUT-"].update("Username is already taken.")
			user_client.set_user(None)
	elif event == "-SIGN_IN-":
		window.close()
		window = sg.Window("Silent Message", login_scene(),
							element_justification='c',
							size=(WIDTH, HEIGHT))
	elif event == "-FRIENDS-" or event == "-ALL_FRIENDS-":
		window.close()
		window = sg.Window("Silent Message",
							friends_list(user_client.get_user()),
							element_justification='c',
							size=(MESSAGE_SCREEN_WIDTH,
									MESSAGE_SCREEN_HEIGHT))
	elif event == "Add Friend":
		window.close()
		window = sg.Window("Silent Message",
							add_friend_scene(user_client.get_user()),
							element_justification='c',
							size=(MESSAGE_SCREEN_WIDTH,
									MESSAGE_SCREEN_HEIGHT))
	elif event == "Send Friend Request":
		user_client.send_friend_request(values)

		# Wait until if sending friend request complete
		while user_client.get_success_code() == None:
			pass
		
		if user_client.get_success_code()== 0:
			window["-FRIEND_ADDED_SUCCESS-"].update("Sent friend request successfully.")
		elif user_client.get_success_code()== 1:
			window["-FRIEND_ADDED_SUCCESS-"].update("Cannot add yourself.")
		elif user_client.get_success_code()== 2:
			window["-FRIEND_ADDED_SUCCESS-"].update("Friend already added.")
		elif user_client.get_success_code()== 3:
			window["-FRIEND_ADDED_SUCCESS-"].update("Friend request is pending.")
		elif user_client.get_success_code()== 4:
			window["-FRIEND_ADDED_SUCCESS-"].update("Username does not exist.")
		
		user_client.reset_success_code()
	elif event == "-PENDING-":
		window.close()
		window = sg.Window("Silent Message",
							pending_friends_scene(user_client.get_user()),
							element_justification='c',
							size=(MESSAGE_SCREEN_WIDTH,
									MESSAGE_SCREEN_HEIGHT))

	if user_client.get_user() != None:
		# Loop through names and check if event match against any of the names pressed
		for friend in user_client.get_user()["friends"]:
			if event == "-{}-".format(friend):
				window.close()
				messages = get_messages(user_client.get_user(), friend)["messages"]
				window = sg.Window("Silent Message",
									message_scene(user_client.get_user(),
													friend, messages),
									element_justification='c',
									size=(MESSAGE_SCREEN_WIDTH,
											MESSAGE_SCREEN_HEIGHT))
		
		for pending in user_client.get_user()["pending"]:
			if event == "-Y_{}-".format(pending["username"]):
				values = {"username": pending["username"], "-ACCEPT-": "YES"}
				user_client.respond_friend_request(values)
				
				# Wait until if sending friend request complete
				while user_client.get_success_code() == None:
					window = sg.Window("Silent Message",
								pending_friends_scene(user_client.get_user()),
								element_justification='c',
								size=(MESSAGE_SCREEN_WIDTH,
										MESSAGE_SCREEN_HEIGHT))
			elif event == "-X_{}-".format(pending["username"]):
				values = {"username": pending["username"], "-ACCEPT-": "NO"}
				user_client.respond_friend_request(values)

				# Wait until if sending friend request complete
				while user_client.get_success_code() == None:
					pass
				
				window.close()
				window = sg.Window("Silent Message",
							pending_friends_scene(user_client.get_user()),
							element_justification='c',
							size=(MESSAGE_SCREEN_WIDTH,
									MESSAGE_SCREEN_HEIGHT))

				window.close()
				window = sg.Window("Silent Message",
							pending_friends_scene(user_client.get_user()),
							element_justification='c',
							size=(MESSAGE_SCREEN_WIDTH,
									MESSAGE_SCREEN_HEIGHT))
			elif event == "-X_{}-".format(pending["username"]):
				values = {"username": pending["username"], "-ACCEPT-": "NO"}
				user_client.respond_friend_request(values)

				# Wait until if sending friend request complete
				while user_client.get_success_code() == None:
					pass
				
				window.close()
				window = sg.Window("Silent Message",
							pending_friends_scene(user_client.get_user()),
							element_justification='c',
							size=(MESSAGE_SCREEN_WIDTH,
									MESSAGE_SCREEN_HEIGHT))

	return window, 0

def start_up():
	# Retrieve Window's Content
	return login_scene()