# Python libraries:
import socket
import sys
from time import sleep

# Global variables for the Client:

client = ""
HOST_ADDRESS = socket.gethostname()
HOST_PORT = 50000 #  Must be the SAME port used for the Server!
MAX_BUFFER = 1024 # 1024 bytes: max buffer size
	

def start_game():

	my_choise = input("\nChoise between [R]ock | [P]aper | [S]cissors -> ")
	while True:
		my_choise = my_choise.upper()
		if my_choise not in ['R', 'P', 'S']:
			print("\nInvalid input! The input can be R\\P\\S!")
			my_choise = input("\nChoise between [R]ock | [P]aper | [S]cissors -> ")
		else:
			# If the input is correct, the player sends his choice to the Server
			client.send(my_choise.encode()) 
			break
		
	# The player receives the Server result and exits the game:
	print(client.recv(MAX_BUFFER).decode())
	sleep(1)
	# If there was a draw, the hand must be replayed:
	if(client.recv(MAX_BUFFER).decode() == 'DRAW'): 
		print("\nThe game ended in a draw! It is necessary to replay!")
		start_game()
	client.close()
	sys.exit()


def connect_player():
	global client

	# Player connect to the Server
	try:
		# Create Client Socket:

		# socket.AF_INET -> IP address: iPv4 type
		# socket.SOCK_STREAM -> TCP protocol
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Client connected to Server:
		client.connect((HOST_ADDRESS, HOST_PORT))
		print("\nThe player is connected for play!")

		# The player writes his name and sends it to the Server
		nickname = input("\nEnter the nickname: ").encode()
		client.send(nickname)


		# The Player receives the welcome message from the Server
		
		while True:
			data = client.recv(MAX_BUFFER).decode()
			
			if data == "Y":
				start_game()


	except socket.error as err:
		print("\nAn error has occurred...", err)
		print("Unable to connect to server! Try later!")
		sys.exit()


if __name__ == "__main__":
	try:
		connect_player()
	except Exception as err:
		print("\nAn error has occurred...", err)
	except KeyboardInterrupt:
		print("\nThe player typed [Ctrl + C] to quit the game!")
		print("\nThe game is over!")