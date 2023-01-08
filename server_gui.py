#-----------------------------------------------------------------------------------------
#									 PYTHON LIBRARIES
#-----------------------------------------------------------------------------------------
import tkinter as tk # for GUI
import socket
import sys
from time import sleep
import threading
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#								GLOBAL VARIABLES FOR THE GAME
#-----------------------------------------------------------------------------------------
players = 0 # counter of the number of players connected to the game
name_player1 = ""
name_player2 = ""
player1_conn = ""
player2_conn = ""
choise_player1 = ""
choise_player2 = ""
draw = 0
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#								GLOBAL VARIABLES FOR THE SERVER
#-----------------------------------------------------------------------------------------
server = ""
MAX_CONNECTION = 2
HOST_ADDRESS = socket.gethostname()
HOST_PORT = 50000 
# NOTE: Choose a port greater than 1024, because ports with lower values are system reserved ports 
MAX_BUFFER = 1024 # 1024 bytes -> max buffer size
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# 									GUI SETTINGS
#-----------------------------------------------------------------------------------------
window = tk.Tk()
window.title('Server Game') # window title

frame = tk.Frame(window)
welcome_txt = 'Welwcome to "Rock, Paper, Scissor" Game!\n'

welcome_lb = tk.Label(frame, text=welcome_txt, fg = "red")
welcome_lb.config(font = ("Courier", 15))
welcome_lb.pack(side=tk.TOP)

message_txt = "___________________________________________\n"
message_txt = message_txt + "Server Messages\n" 
message_txt = message_txt + "___________________________________________"
message_lb = tk.Label(frame, text=message_txt, fg = "blue")
message_lb.config(font = ("Courier", 11))
message_lb.pack(side=tk.TOP)

start_button = tk.Button(frame, text="Start", command=lambda:connect_server())
start_button.pack(side=tk.BOTTOM)


server_message_txt = ""
server_message_lb = tk.Label(frame, text = server_message_txt, fg = "black")
server_message_lb.config(font = ("Courier", 10))
server_message_lb.pack(side = tk.TOP)

frame.pack(side=tk.TOP, pady=(5, 0))
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#										GUI METHOD
#-----------------------------------------------------------------------------------------

def update_server_message(msg):
	global server_message_txt # Update server_message_lb
	#server_message_txt = server_message_txt + msg + "\n\n"
	server_message_txt = msg + "\n\n"
	server_message_lb["text"] = server_message_txt
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#										GAME METHOD
#-----------------------------------------------------------------------------------------

def get_winner(choise_player1, choise_player2, name_player1, name_player2):

	'''
		*** GAME RULES ***

		1. [R]ock breaks [S]cissors ([R]ock wins)
		2. [S]cissors cut [P]aper ([S]cissors win)
		3. [P]aper wraps [R]ock ([P]aper wins)
		If there was a draw (the players make the same choise),
		 the hand must be replayed:

	'''

	global draw

	msg = "The system is about to proclaim the winner..."
	logging.info(msg)
	update_server_message(msg)
	result = "\n***FINAL RESULTS***\n\n"
	if (choise_player1 == 'R' and choise_player2 == 'P'
		or choise_player1 == 'P' and choise_player2 == 'S'
			or choise_player1 == 'S' and choise_player2 == 'R'):
				result = result + "[Player 1: " + name_player1 + " - Choise: " + choise_player1 + "]\n" 
				result = result + "[Player 2: " + name_player2 + " - Choise: " + choise_player2 + "]\n"
				result = result + "\nRESULT: " + name_player2 + " won "+ name_player1 + "!\n"
	elif (choise_player1 == 'S' and choise_player2 == 'S'
			or choise_player1 == 'P' and choise_player2 == 'P'
			or choise_player1 == 'R' and choise_player2 == 'R'):
			draw = 1
			result = result + "[Player 1: " + name_player1 + " - Choise: " + choise_player1 + "]\n" 
			result = result + "[Player 2: " + name_player2 + " - Choise: " + choise_player2 + "]\n"
			result = result + "\nRESULT: DRAW!\n"
	else:
		result = result + "[Player 1: " + name_player1 + " - Choise: " + choise_player1 + "]\n" 
		result = result + "[Player 2: " + name_player2 + " - Choise: " + choise_player2 + "]\n"
		result = result + "\nRESULT: " + name_player1 + " won "+ name_player2 + "!\n"

	return result

def start_game():
	global choise_player1, choise_player2, draw


	# Il The Server is waiting for the choices from two players:
	# rock, paper or scissors

	msg = "Waiting to receive a choice from the two players!"
	logging.info(msg)
	update_server_message(msg)

	# The Server receives the choice of the first player
	choise_player1 = player1_conn.recv(MAX_BUFFER).decode()
	msg = "A choice has been made! Looking forward to the second..."
	logging.info(msg)
	update_server_message(msg)

	choise_player2 = player2_conn.recv(MAX_BUFFER).decode()
	msg = "The second choice has been received!"
	logging.info(msg)
	update_server_message(msg)

	result = get_winner(choise_player1, choise_player2, name_player1, name_player2)

	# The server sends the players the choices made by both and the name of the winner

	logging.info(result)
	update_server_message(result)

	player1_conn.send(result.encode())
	player2_conn.send(result.encode())

	# If there was a draw, the hand must be replayed:
	if draw == 1:
		msg = "The game ended in a draw! It is necessary to replay!"
		logging.info(msg)
		update_server_message(msg)
		player1_conn.send("DRAW".encode())
		player2_conn.send("DRAW".encode())
		draw = 0
		sleep(1)
		start_game()

	server.close()
	sys.exit()

def connect_players(server, y):
	global players, name_player1, name_player2, player1_conn, player2_conn
	
	# The Server is ready to receive "messages" from the Client
	while True:
		connection_client, address_client = server.accept() 
		players += 1 # player counter increased
		if players == 1: 
			# One player connected
			name_player1 = connection_client.recv(MAX_BUFFER).decode()
			player1_conn = connection_client
			msg = "Player 1 (" + name_player1 + "), connected to game!"
			logging.info(msg)
			update_server_message(msg)
			
			# The server sends a Welcome message to Player 1
			messaggio = "Welcome! Waiting for Player 2!"
			connection_client.send(messaggio.encode())
		elif players == 2:
			# Two players connected
			name_player2 = connection_client.recv(MAX_BUFFER).decode()
			player2_conn = connection_client
			msg = "Player 2 (" + name_player2 + "), connected to game!"
			logging.info(msg)
			update_server_message(msg)

			# The server sends a Welcome message to Player 2
			messaggio = "Welcome!"
			connection_client.send(messaggio.encode())

			break

	# If there are two players connected, the game can start
	msg = "Two players are connected! The game will starts in 5 seconds..."
	logging.info(msg)
	update_server_message(msg)
	sleep(5)
	player1_conn.send("Y".encode())
	player2_conn.send("Y".encode())
	start_game()



def connect_server():
	global server

	msg = '\nWelcome to "[R]ock, [P]aper, [S]cissors" game!'
	logging.info(msg)
	# Manage any exceptions (e.g. port already used by another service)
	try:
		# Create Server socket:

		# socket.AF_INET -> IP address: iPv4 type
		# socket.SOCK_STREAM -> TCP protocol
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connecting the socket to the machine address and designated port
		server.bind((HOST_ADDRESS, HOST_PORT))

		# The server listens for a possible player
		# NOTE: In this case the server can manage atmost two connections simultaneously
		server.listen(MAX_CONNECTION) # MAX_CONNECTION = 2

		msg = "The Server has been initialized!"
		msg = msg + "\nThe server is waiting for " + str(MAX_CONNECTION) + " players..."
		logging.info(msg)
		update_server_message(msg)

		# If no errors occurred, the player is accepted by the Server
		
		# Create new thread, otherwise gui thread is blocked
		threading._start_new_thread(connect_players, (server, " "))

		
	except socket.error as err:
		msg = "An error has occurred..." + str(err)
		msg = msg + "\nI'm trying to reinitialize the server..."
		logging.info(msg)
		update_server_message(msg)
		# Recursive call to the function to try to reconnect the server
		connect_server()

#-----------------------------------------------------------------------------------------


if __name__ == '__main__':
	try:
		window.mainloop()
	except socket.error as err:
		msg = "An error has occurred..." + str(err)
		msg = msg + "\nI'm trying to reinitialize the server..."
		logging.info(msg)
		update_server_message(msg)
		sys.exit()
	except KeyboardInterrupt:
		msg = "The player typed [Ctrl + C] to quit the game!"
		msg = msg + "\nThe game is over!"
		logging.info(msg)
		update_server_message(msg)
		sys.exit()