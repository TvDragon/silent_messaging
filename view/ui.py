import PySimpleGUI as sg
from os import getcwd
import sys

path = getcwd()[:-4]
sys.path.insert(0, "{}controller/".format(path))

from events_handler import *

sg.theme('DarkAmber')	# Add a little color to your windows

# Define the window's contents
sign_up = [[sg.Text("Sign Up", font=("Arial", 20))],
		[sg.Text(size=(40,1), key="-OUTPUT-", text_color="yellow")],
		[sg.Text("Full Name"), sg.Input(key="-FULL_NAME-", size=(30, 1),
			text_color="white")],
		[sg.Text("Username"), sg.Input(key="-USERNAME-", size=(30, 1),
			text_color="white")],
		[sg.Text("Email\t"), sg.Input(key="-EMAIL-", size=(30, 1),
			text_color="white",)],
		[sg.Text("Password"), sg.Input(key="-PASSWORD-", size=(30, 1),
			password_char="*", text_color="white")],
		[sg.Button("Sign Up")],
		[sg.Text("Already Have an Account?"), sg.Button("Sign In")]]

# Create the window
window = sg.Window('Silent Message', sign_up, element_justification='c', size=(512, 240))

# Display and interact with the Window using an Event Loop
while True:
	event, values = window.read()
	# See if user wants to quit or window was closed
	if event == sg.WINDOW_CLOSED:
		break
	if event == "Sign Up":
		username_taken = add_user(values)
		
		if not username_taken:
			window["-OUTPUT-"].update("")
		else:
			window["-OUTPUT-"].update("Username is already taken.")


# Finish up by removing from the screen
window.close()