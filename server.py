# Python libraries:
import socket
import sys
from time import sleep


# Global variables for the game:

players = 0 # counter of the number of players connected to the game
name_player1 = ""
name_player2 = ""
player1_conn = ""
player2_conn = ""
choise_player1 = ""
choise_player2 = ""
draw = 0


# Global variables for the Server:
server = ""
MAX_CONNECTION = 2
HOST_ADDRESS = socket.gethostname()
HOST_PORT = 50000 
# NOTE: Choose a port greater than 1024, because ports with lower values are system reserved ports 
MAX_BUFFER = 1024 # 1024 bytes -> max buffer size



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

	print("The system is about to proclaim the winner...")
	result = "\n***FINAL RESULTS***\n"
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
			result = result + "\nDRAW!\n"
	else:
		result = result + "[Player 1: " + name_player1 + " - Choise: " + choise_player1 + "]\n" 
		result = result + "[Player 2: " + name_player2 + " - Choise: " + choise_player2 + "]\n"
		result = result + "\nRESULT: " + name_player1 + " won "+ name_player2 + "!\n"

	return result

def start_game():
	global choise_player1, choise_player2, draw


	# Il The Server is waiting for the choices from two players:
	# rock, paper or scissors

	print("\nWaiting to receive a choice from the two players!")

	# The Server receives the choice of the first player
	choise_player1 = player1_conn.recv(MAX_BUFFER).decode()
	print("\nA choice has been made! Looking forward to the second...")

	choise_player2 = player2_conn.recv(MAX_BUFFER).decode()
	print("The second choice has been received!")
	result = get_winner(choise_player1, choise_player2, name_player1, name_player2)

	# The server sends the players the choices made by both and the name of the winner

	print(result)

	player1_conn.send(result.encode())
	player2_conn.send(result.encode())

	# If there was a draw, the hand must be replayed:
	if draw == 1:
		print("\nThe game ended in a draw! It is necessary to replay!")
		sleep(1)
		player1_conn.send("DRAW".encode())
		player2_conn.send("DRAW".encode())
		draw = 0
		start_game()
		


	server.close()
	sys.exit()


def connect_server():
	global server, players, name_player1, name_player2, player1_conn, player2_conn

	print('\nWelcome to "[R]ock, [P]aper, [S]cissors" game!\n\n')

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

		print("\nThe Server has been initialized!")
		print("The server is waiting for two players", MAX_CONNECTION, "players!")

		# If no errors occurred, the player is accepted by the Server
		
		

		# The Server is ready to receive "messages" from the Client
		while True:
			connection_client, address_client = server.accept() 
			players += 1 # player counter increased
			if players == 1: 
				# One player connected
				name_player1 = connection_client.recv(MAX_BUFFER).decode()
				player1_conn = connection_client
				print("\nPlayer 1 (", name_player1, "), connected to game!")
				
				
				# The server sends a Welcome message to Player 1
				messaggio = "Welcome! Waiting for Player 2!"
				connection_client.send(messaggio.encode())

			elif players == 2:
				# Two players connected
				name_player2 = connection_client.recv(MAX_BUFFER).decode()
				player2_conn = connection_client
				print("Player 2 (", name_player2, "), connected to game!")


				# The server sends a Welcome message to Player 2
				messaggio = "Welcome!"
				connection_client.send(messaggio.encode())

				break

		# If there are two players connected, the game can start
		print("\nTwo players are connected! The game will starts in 5 seconds...")
		sleep(5)
		player1_conn.send("Y".encode())
		player2_conn.send("Y".encode())
		start_game()


	except socket.error as err:
		print("\nAn error has occurred...", err)
		print("\nI'm trying to reinitialize the server...")
		# Recursive call to the function to try to reconnect the server
		connect_server()
		

if __name__ ==  "__main__":
	try:
		connect_server();
	except Exception as err:
		print("\nAn error has occurred...", err)
	except KeyboardInterrupt:
		print("\nThe player typed [Ctrl + C] to quit the game!")
		print("\nThe game is over!")
	