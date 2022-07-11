from game import Game
from player import Player
from player1 import Player1
from player2 import Player2
from random import randrange


if __name__ == "__main__":#This is where you decided which player gets what AI
	"Test Game"

	p1 = Player2("Henry")
	p3 = Player2("Paul")

	p2 = Player1("Alex")
	p4 = Player1("Sarah")

	"Control Game"
	p1a = Player1("HenryA")
	p3a = Player1("PaulA")

	p2a = Player1("AlexA")
	p4a = Player1("SarahA")

	team1Score = 0
	team1aScore = 0

	numGames = 1
	neededScore = 10
	printOutput = True#Whether or not each hand is printed in the console

	for index in range(numGames):
		randSeed = randrange(-10000,10000)

		gTest = Game([p1, p2, p3, p4])
		team1Score+=gTest.play_game(neededScore, randSeed, printOutput)

		gControl = Game([p1a, p2a, p3a, p4a])
		team1aScore+=gControl.play_game(neededScore, randSeed, printOutput)

	print "team 1 won ",team1Score," games out of ", numGames
	print "team 1a won ",team1aScore," games out of ", numGames
