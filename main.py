import utils
from game import Game
from player import Player
from player1 import Player1
from player2 import Player2
from player3 import Player3
from random import randrange

import copy


if __name__ == "__main__":#This is where you decided which player gets what AI
	"Test Game"
	p1 = Player3("Henry")
	p3 = Player3("Paul")

	p2 = Player("Alex")
	p4 = Player("Sarah")

	"Control Game"
	p1a = Player("HenryA")
	p3a = Player("PaulA")

	p2a = Player("AlexA")
	p4a = Player("SarahA")

	team1Score = 0
	team1aScore = 0

	numGames = 100#Number of games played
	neededScore = 10#Number of points needed to win a game
	printOutput = False#Whether or not each hand is printed in the console


	for index in range(numGames):
		randSeed = randrange(-10000,10000)

		gTest = Game([p1, p2, p3, p4])
		team1Score+=gTest.play_game(neededScore, randSeed, printOutput)

		gControl = Game([p1a, p2a, p3a, p4a])
		team1aScore+=gControl.play_game(neededScore, randSeed, printOutput)

	print "team 1 won ",team1Score," games out of ", numGames
	print "team 1a won ",team1aScore," games out of ", numGames