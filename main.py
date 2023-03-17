import utils
from game import Game
from player import Player
from player1 import Player1
from player1B import Player1B
from player2 import Player2
from player3 import Player3
from player4 import Player4
from player4B import Player4B
from random import randrange

from playerTest import PlayerTest

import copy


if __name__ == "__main__":#This is where you decided which player gets what AI
	"Test Game"
	p1 = PlayerTest("Henry")
	p3 = PlayerTest("Paul")

	p2 = Player4B("Alex")
	p4 = Player4B("Sarah")

	"Second Test Game"
	#p1t = PlayerTest("HenryT")
	#p3t = PlayerTest("PaulT")

	#p2t = Player3("AlexT")
	#p4t = Player3("SarahT")

	"Control Game"
	p1a = Player4B("HenryA")
	p3a = Player4B("PaulA")

	p2a = Player4B("AlexA")
	p4a = Player4B("SarahA")

	team1Score = 0
	#team1tScore = 0
	team1aScore = 0

	numGames = 100#Number of games played
	neededScore = 10#Number of points needed to win a game
	printOutput = False#Whether or not each hand is printed in the console


	for index in range(numGames):
		randSeed = randrange(-10000,10000)

		gTest = Game([p1, p2, p3, p4])
		team1Score+=gTest.play_game(neededScore, randSeed, printOutput)

	#	gTest2 = Game([p1t, p2t, p3t, p4t])
	#	team1tScore+=gTest2.play_game(neededScore, randSeed, printOutput)

		gControl = Game([p1a, p2a, p3a, p4a])
		team1aScore+=gControl.play_game(neededScore, randSeed, printOutput)

	print "team 1 won ",team1Score," games out of ", numGames
	#print "team 1t won ",team1tScore," games out of ", numGames
	print "team 1a won ",team1aScore," games out of ", numGames