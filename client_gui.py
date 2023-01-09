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
my_choise = ""
nickname = "x"
opponent_player = "x"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#								GLOBAL VARIABLES FOR THE CLIENT
#-----------------------------------------------------------------------------------------
client = ""
HOST_ADDRESS = socket.gethostname()
HOST_PORT = 50000 #  Must be the SAME port used for the Server!
MAX_BUFFER = 1024 # 1024 bytes: max buffer size
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# 									GUI SETTINGS
#-----------------------------------------------------------------------------------------
window = tk.Tk()
window.title('Client Game') # window title


frame = tk.Frame(window)
welcome_txt = 'Welcome to "Rock, Paper, Scissor" Game!\n\n'
welcome_lb = tk.Label(frame, text=welcome_txt, fg = "red")
welcome_lb.config(font = ("Courier", 15))
welcome_lb.pack(side=tk.TOP)

player_name_lb = tk.Label(frame, text = "Name")
player_name_lb.config(font = ("Courier", 11))
player_name_lb.pack(side = tk.LEFT)

player_name_etn = tk.Entry(frame)
player_name_etn.pack(side = tk.LEFT)

player_name_btn = tk.Button(frame, text = "Connect", command = lambda:connect_player())
player_name_btn.pack(side = tk.LEFT)

frame.pack(side=tk.TOP, pady=(5, 0))

frame_info = tk.Frame()
you_opponent_txt = "\n\nYou: " + nickname + " - Opponent Player: " + opponent_player
you_opponent_lb = tk.Label(frame_info, text = you_opponent_txt)
you_opponent_lb .config(font = ("Courier", 11))
you_opponent_lb .pack(side = tk.LEFT)
frame_info.pack(side=tk.TOP, pady=(5, 0))

button_frame = tk.Frame(window)
	
img_rock = tk.PhotoImage(file = r"img/rock.png")
img_rock = img_rock.subsample(3, 3) # resize image button

img_paper = tk.PhotoImage(file = r"img/paper.png")
img_paper = img_paper.subsample(3, 3) # resize image button

img_scissors = tk.PhotoImage(file = r"img/scissors.png")
img_scissors = img_scissors.subsample(3, 3) # resize image button

btn_rock = tk.Button(
	button_frame,
	text = "Rock",
	command = lambda:choise("R"),
	state = tk.DISABLED,
	image = img_rock
)

btn_paper = tk.Button(
	button_frame,
	text = "Paper",
	command = lambda:choise("P"),
	state = tk.DISABLED,
	image = img_paper
)
	
btn_scissors = tk.Button(
	button_frame,
	text = "Scissors",
	command = lambda:choise("S"),
	state = tk.DISABLED,
	image = img_scissors
)
	

btn_rock.grid(row = 0, column = 0)
btn_paper.grid(row = 0, column = 1)
btn_scissors.grid(row = 0, column = 2)
button_frame.pack(side = tk.BOTTOM)


game_frame = tk.Frame(window)

message_game_tx = "\n___________________________________________\n"
message_game_tx = message_game_tx + "GAME INFORMATION\n"
message_game_tx = message_game_tx + "___________________________________________\n"
message_game = tk.Label(game_frame, text = message_game_tx, fg = "blue",font = ("Courier", 11))
message_game.pack()

result_lb_txt = " "
result_lb = tk.Label(game_frame, text = result_lb_txt, fg = "black",font = ("Courier", 10))
result_lb.pack()
game_frame.pack(side = tk.TOP)

#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#										GUI METHOD
#-----------------------------------------------------------------------------------------
def enable_button(choise):
	if choise == "y":
		btn_rock.config(state=tk.NORMAL)
		btn_paper.config(state=tk.NORMAL)
		btn_scissors.config(state=tk.NORMAL)
	else:
		btn_rock.config(state=tk.DISABLED)
		btn_paper.config(state=tk.DISABLED)
		btn_scissors.config(state=tk.DISABLED)


def update_client_message(msg):
	global result_lb_txt
	#result_lb_txt = msg + "\n\n"
	result_lb_txt = result_lb_txt + msg + "\n\n"
	result_lb['text'] = result_lb_txt

def update_client_gui():
	global you_opponent_txt

	you_opponent_txt = "You: " + nickname + " - Opponent Player: " + opponent_player
	you_opponent_lb['text'] = you_opponent_txt
	
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
#										GAME METHOD
#-----------------------------------------------------------------------------------------

def get_winner(client, y):
	winner = client.recv(MAX_BUFFER).decode()
	#sleep(1)
	if winner == nickname:
		winner = "YOU WIN!"
	elif winner == opponent_player:
		winner = "YOU LOSE"
	
	logging.info(winner)
	update_client_message(winner)

	if winner == "DRAW":
		msg = "The game ended in a draw!\n It is necessary to replay!"
		logging.info(msg)
		update_client_message(msg)
		sleep(3)
		enable_button("y") 

def choise(choise):
	global my_choise

	enable_button("n")
	
	my_choise = choise
	my_choise = my_choise.upper()

	if my_choise in ['R', 'P', 'S']:
		msg = "Your choise: " + str(my_choise)
		#logging.info(msg)
		#update_client_message(msg)
		client.send(my_choise.encode())
	
	# Create new thread, otherwise gui thread is blocked
	threading._start_new_thread(get_winner, (client, " "))


def start_game(client, y):
	global nickname, opponent_player
	frame.pack_forget()
	# The player writes his name and sends it to the Server
	nickname = player_name_etn.get()
	client.send(nickname.encode())
	msg = "Your nickname: " + nickname
	logging.info(msg)
	update_client_message(msg)
	
	# The Player receives the welcome message from the Server 
	while True:
		data = client.recv(MAX_BUFFER).decode()
		if data == "Y":
			msg = "The game can be start."
			msg = msg + "\nChoise between Rock, Paper or Scissors!"
			logging.info(msg)
			update_client_message(msg)
			sleep(2)
			enable_button("y")
			break
	# Client legge il nome dello sfidante
	opponent_player = client.recv(MAX_BUFFER).decode()
	msg = "Opponent Player: " + opponent_player
	logging.info(msg)
	update_client_message(msg)
	update_client_gui()

def connect_player():
	# Player connect to the Server
	global client

	try:
		# Create Client Socket:

		# socket.AF_INET -> IP address: iPv4 type
		# socket.SOCK_STREAM -> TCP protocol
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Client connected to Server:
		client.connect((HOST_ADDRESS, HOST_PORT))
		msg = "\nYou are connect for playing"
		logging.info(msg)
		update_client_message(msg)

		# Create new thread, otherwise gui thread is blocked
		threading._start_new_thread(start_game, (client, " "))

	except socket.error as err:
		msg = "An error has occurred...\n" + str(err)
		msg = msg + "\nUnable to connect to server! Try later!"
		logging.info(msg)
		update_client_message(msg)
		#sleep(5)
		#sys.exit()
	
#-----------------------------------------------------------------------------------------

if __name__ == '__main__':
	try:
		window.mainloop()
		sys.exit()
		client.exit()
	except socket.error as err:
		msg = "An error has occurred..." + str(err)
		msg = msg + "\nUnable to connect to server! Try later!"
		logging.info(msg)
		update_client_message(msg)
		sleep(5)
		sys.exit()
	except KeyboardInterrupt:
		msg = "The player typed [Ctrl + C] to quit the game!"
		msg = msg + "\nThe game is over!"
		logging.info(msg)
		update_client_message(msg)