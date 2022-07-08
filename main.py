from game import Game
from player import Player
from player1 import Player1
from random import randrange


if __name__ == "__main__":#This is where you decided which player gets what AI
	p1 = Player1("Henry")
	p2 = Player("Alex")
	p3 = Player("Paul")
	p4 = Player("Sarah")

	p1a = Player("HenryA")
	p2a = Player("AlexA")
	p3a = Player("PaulA")
	p4a = Player("SarahA")

	player1Score = 0
	playerScore = 0
	for index in range(1000):
		randSeed = randrange(-10000,10000)

		g1 = Game([p1, p2, p3, p4])
		player1Score+=g1.play_game(1, randSeed)

		g2 = Game([p1a, p2a, p3a, p4a])
		playerScore+=g2.play_game(1, randSeed)

	print("p1 won ",player1Score," games out of 1000")
	print("p1a won ",playerScore," games out of 1000")
