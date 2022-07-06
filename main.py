from game import Game
from player import Player
from player1 import Player1


if __name__ == "__main__":#This is where you decided which player gets what AI
	p1 = Player1("Henry")
	p2 = Player("Alex")
	p3 = Player("Paul")
	p4 = Player("Sarah")

	g = Game([p1, p2, p3, p4])
	g.play_game()
