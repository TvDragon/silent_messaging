import PySimpleGUI as sg
from controller import handle_events, start_up
from view import WIDTH, HEIGHT

def start_app(user_client):

	sg.theme('DarkAmber')	# Add a little color to your windows

	# Create the window
	window = sg.Window("Silent Message", start_up(), element_justification='c',
						size=(WIDTH, HEIGHT))

	# Display and interact with the Window using an Event Loop
	while True:
		event, values = window.read()
		window, exit_code = handle_events(event, values, user_client, window)

		if exit_code == 1:
			break

	# Finish up by removing from the screen
	window.close()