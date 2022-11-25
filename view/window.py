import PySimpleGUI as sg
from os import getcwd
import sys
import json

path = getcwd()

sys.path.insert(0, "{}/controller/".format(path))

from events_handler import *

WIDTH = 512
HEIGHT = 240
MESSAGE_SCREEN_WIDTH = 1280
MESSAGE_SCREEN_HEIGHT = 960

def sign_up_scene():
	return [[sg.Text("Sign Up", font=("Arial", 20))],
			[sg.Text(key="-OUTPUT-", text_color="yellow")],
			[sg.Text("Full Name"), sg.Input(key="-FULL_NAME-", size=(30, 1),
				text_color="white")],
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
			sg.Column(message, size=(MESSAGE_SCREEN_WIDTH - 200, MESSAGE_SCREEN_HEIGHT))]]

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
			sg.Column(find_user, size=(MESSAGE_SCREEN_WIDTH - 200, MESSAGE_SCREEN_HEIGHT))]]

def friends_list(user):

	recent_dms = recent_messages(user)

	friends_ls = [[sg.Text("Friends", font=("Arial", 20)),
					sg.Button("Add Friend")
			]]

	friends = user["friends"]

	for friend in friends:
		friends_ls.append([sg.Text("{}".format(friend), key="-{}-".format(friend),
							enable_events=True, font=("Arial", 14),
							text_color="grey")])

	return [[sg.Column(recent_dms, size=(200, MESSAGE_SCREEN_WIDTH)),
			sg.Column(friends_ls, size=(MESSAGE_SCREEN_WIDTH - 200, MESSAGE_SCREEN_HEIGHT))]]

def start_app():

	sg.theme('DarkAmber')	# Add a little color to your windows

	# Define the window's contents
	login = login_scene()

	# Create the window
	window = sg.Window("Silent Message", login, element_justification='c',
						size=(WIDTH, HEIGHT))

	friend_tmp = {
        "name": "Bob Do",
        "username": "BobD",
        "hashed password": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
        "friends": []
    }
	curr_user = None

	# Display and interact with the Window using an Event Loop
	while True:
		event, values = window.read()
		# See if user wants to quit or window was closed
		if event == sg.WINDOW_CLOSED:
			break
		if event == "Sign In":
			found_user, user = find_user(values)

			if found_user:
				window.close()
				window = sg.Window("Silent Message", friends_list(user),
									size=(MESSAGE_SCREEN_WIDTH, MESSAGE_SCREEN_HEIGHT))
				curr_user = user
			else:
				window["-OUTPUT-"].update("Username or Password may be incorrect. User may not exist.")
		if event == "-SIGN_UP-":
			window.close()
			window = sg.Window("Silent Message", sign_up_scene(),
								element_justification='c',
								size=(WIDTH, HEIGHT))
		if event == "Sign Up":
			username_taken, new_user = add_user(values)
			
			if not username_taken:
				window.close()
				window = sg.Window("Silent Message", friends_list(new_user),
									element_justification='c',
									size=(MESSAGE_SCREEN_WIDTH, MESSAGE_SCREEN_HEIGHT))
				curr_user = new_user
			else:
				window["-OUTPUT-"].update("Username is already taken.")
		if event == "-SIGN_IN-":
			window.close()
			window = sg.Window("Silent Message", login_scene(),
								element_justification='c',
								size=(WIDTH, HEIGHT))
		if event == "-FRIENDS-":
			window.close()
			window = sg.Window("Silent Message", friends_list(curr_user),
								element_justification='c',
								size=(MESSAGE_SCREEN_WIDTH, MESSAGE_SCREEN_HEIGHT))
		if event == "Add Friend":
			window.close()
			window = sg.Window("Silent Message", add_friend_scene(curr_user),
								element_justification='c',
								size=(MESSAGE_SCREEN_WIDTH, MESSAGE_SCREEN_HEIGHT))
		if event == "Send Friend Request":
			success = add_friend(curr_user, values)
			
			if success:
				window["-FRIEND_ADDED_SUCCESS-"].update("Added friend successfully.")
			else:
				window["-FRIEND_ADDED_SUCCESS-"].update("Username doesn't exist.")

		if curr_user != None:
			# Loop through names and check if event match against any of the names pressed
			for friend in curr_user["friends"]:
				if event == "-{}-".format(friend):
					window.close()
					window = sg.Window("Silent Message", message_scene(curr_user, friend),
										element_justification='c',
										size=(MESSAGE_SCREEN_WIDTH, MESSAGE_SCREEN_HEIGHT))

	# Finish up by removing from the screen
	window.close()