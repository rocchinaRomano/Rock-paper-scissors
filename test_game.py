import unittest

from server_gui import get_winner

class TestGame(unittest.TestCase):

	name_player2 = "Paperino"
	name_player1 = "Pippo"

	def test_get_winner_draw1(self):
	
		choise_player1 = 'R'
		choise_player2 = 'R'

		result = "DRAW"

		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)
		
		self.assertEqual(result, result_server)

	
	def test_get_winner_draw2(self):
		
		choise_player1 = 'P'
		choise_player2 = 'P'

		result = "DRAW"

		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)
		
		self.assertEqual(result, result_server)
	
	def test_get_winner_draw3(self):
		
		choise_player1 = 'S'
		choise_player2 = 'S'

		result = "DRAW"

		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)
		
		self.assertEqual(result, result_server)

	
	def test_get_winner_rock1(self):
		# [R]ock breaks [S]cissors -> [R]ock wins
		choise_player1 = 'R'
		choise_player2 = 'S'

		result = self.name_player1
		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)

		self.assertEqual(result, result_server)		

	
	def test_get_winner_rock2(self):
		# [R]ock breaks [S]cissors ->  [R]ock wins
		choise_player1 = 'S'
		choise_player2 = 'R'

		result = self.name_player2
		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)

		self.assertEqual(result, result_server)		

	
	
	def test_get_winner_scissors1(self):
		# [S]cissors cut [P]aper -> [S]cissors win	
		choise_player1 = 'S'
		choise_player2 = 'P'

		result = self.name_player1
		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)

		self.assertEqual(result, result_server)		

	
	def test_get_winner_scissors2(self):
		# [S]cissors cut [P]aper -> [S]cissors win	
		choise_player1 = 'P'
		choise_player2 = 'S'

		result = self.name_player2
		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)

		self.assertEqual(result, result_server)		


	def test_get_winner_paper1(self):
		#[P]aper wraps [R]ock -> [P]aper wins
		choise_player1 = 'P'
		choise_player2 = 'R'

		result = self.name_player1
		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)

		self.assertEqual(result, result_server)		
	
	def test_get_winner_paper2(self):
		#[P]aper wraps [R]ock -> [P]aper wins
		choise_player1 = 'R'
		choise_player2 = 'P'

		result = self.name_player2
		result_server = get_winner(choise_player1, choise_player2, self.name_player1, self.name_player2)

		self.assertEqual(result, result_server)		
	
if __name__ == "__main__":
	unittest.main()