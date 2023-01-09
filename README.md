# "Rock, Paper, Scissors" Game

**Python** Client-Server Application of "**Rock, Paper, Scissors**" game.

### GAME RULES:

1. [R]ock breaks [S]cissors  &ensp;&ensp; -> &ensp; [R]ock wins
2. [S]cissors cut [P]aper   &ensp;&ensp;&ensp;&ensp; -> &ensp; [S]cissors win
3. [P]aper wraps [R]ock      &ensp;&ensp;&ensp;&ensp; -> &ensp; [P]aper wins

If there was a **DRAW** (the players make the same choise), the hand must be replayed.

### SEQUENCE DIAGRAM OF GAME:

<img src="/img/sequence_diagram.jpg">

## PREREQUISITES

- [Anaconda](https://www.anaconda.com/products/distribution)

&ensp;&ensp;&ensp; or 

- [Python](https://www.python.org/downloads/)

**NOTE**: Use **python 3.8** version or higher!

### Python Libraries Installation

Install **Tkinter** library for GUI:

- for **Windows**:

```console
   pip install tk
```  

- for **Linux**:

```console
   sudo apt-get install -y python3-tk
```  


# GAME INSTALLATION 


**1.** Clone repository

```console
   git clone https://github.com/rocchinaRomano/Rock-paper-scissors.git
```  
     
        
&ensp;&ensp;&ensp;&ensp;**Otherwise**: Download all contents of ["Rock-paper-scissors"](https://github.com/rocchinaRomano/Rock-paper-scissors) repository (On "Code", "Download ZIP")

**2.** After download, unzip "**Rock-paper-scissors-main.zip**" folder

# HOW TO PLAY

**1.** In the "**Rock-paper-scissors-main**" folder, open **three** "Anaconda or Python shell":

   - One for the Server
   - Two for the two Players: "*Player 1*" and "*Player 2*"

**2.** In the **Server shell** type the following command:

```console
   python3 server_gui.py
```  

**3.** In the two **Players shell** type following command:

```console
   python3 client_gui.py
```  

**4.** The **two Players** enter their nickname and the game can be start

**5.** The players make a choise between "**[R]ock, [P]aper or [S]cissors"** and the server proclaims the **winner** according to the game rules.

**NOTE**: In **DRAW** case (the two players make the **same choice**), the two players must replay.

   
# VIDEO TUTORIAL OF GAME

A step-by-step video tutorial of game is available [here](https://github.com/rocchinaRomano/Rock-paper-scissors/blob/video_tutorial/game_tutorial_GUI.mp4).


# A SHELL VERSION OF GAME

[Here](https://github.com/rocchinaRomano/Rock-paper-scissors/tree/shell_game) is also available a **shell** version of game.

# REGRESSION TEST

## Prerequisities: 

Python "**unittest**"  library

## Run regression test:

In the "**Rock-paper-scissors-main**" folder open one "Anaconda or Python shell" and type the following command:

```console
   python3 test_game.py
```
