import PySimpleGUI as sg
from os import getcwd
import sys

path = getcwd()

sys.path.insert(0, "{}/controller/".format(path))

from events_handler import *

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

def message_scene():
	pass

def start_app():

	sg.theme('DarkAmber')	# Add a little color to your windows

	# Define the window's contents
	login = login_scene()

	# Create the window
	window = sg.Window("Silent Message", login, element_justification='c',
						size=(512, 240))

	# Display and interact with the Window using an Event Loop
	while True:
		event, values = window.read()
		# See if user wants to quit or window was closed
		if event == sg.WINDOW_CLOSED:
			break
		if event == "Sign In":
			found_user = find_user(values)

			if found_user:
				window["-OUTPUT-"].update("")
			else:
				window["-OUTPUT-"].update("Username or Password may be incorrect. User may not exist.")
		if event == "-SIGN_UP-":
			window.close()
			window = sg.Window("Silent Message", sign_up_scene(),
								element_justification='c',
								size=(512, 240))
		if event == "Sign Up":
			username_taken = add_user(values)
			
			if not username_taken:
				window.close()
				window = sg.Window("Slient Message", message_scene(),
									element_justification='c',
									size=(512, 240))
			else:
				window["-OUTPUT-"].update("Username is already taken.")
		if event == "-SIGN_IN-":
			window.close()
			window = sg.Window("Silent Message", login_scene(),
								element_justification='c',
								size=(512, 240))


	# Finish up by removing from the screen
	window.close()