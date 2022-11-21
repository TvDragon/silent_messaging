import PySimpleGUI as sg
from hashlib import sha256
from user import User

users = []

# Define the window's contents
sign_up = [[sg.Text("Sign Up")],
		  [sg.Text(size=(40,1), key="-OUTPUT-", text_color="yellow")],
		  [sg.Text("Full Name"), sg.Input(key="-FULL_NAME-", size=(30, 1))],
		  [sg.Text("Username"), sg.Input(key="-USERNAME-", size=(30, 1))],
		  [sg.Text("Email\t"), sg.Input(key="-EMAIL-", size=(30, 1))],
		  [sg.Text("Password"), sg.Input(key="-PASSWORD-", size=(30, 1),
		  	password_char="*")],
		  [sg.Button("Sign Up")],
		  [sg.Text("Already Have an Account?"), sg.Button("Sign In")]]

# Create the window
window = sg.Window('Silent Message', sign_up, element_justification='c')

# Display and interact with the Window using an Event Loop
while True:
	event, values = window.read()
	# See if user wants to quit or window was closed
	if event == sg.WINDOW_CLOSED:
		break
	if event == "Sign Up":
		hashed_password = sha256(values["-PASSWORD-"].encode('utf-8')).hexdigest()
		new_user = User(values["-FULL_NAME-"], values["-USERNAME-"],
						values["-EMAIL-"], hashed_password)
		username_taken = False
		for user in users:
			if new_user.get_username() == user.get_username():
				# Output a message to the window
				window["-OUTPUT-"].update('Username ' + values["-USERNAME-"] + " is already taken.")
				username_taken = True
				break
		if not username_taken:
			window["-OUTPUT-"].update("")
			users.append(new_user)

		print(users)


# Finish up by removing from the screen
window.close()