import utils
from game import Game
from gamestate import Gamestate
import copy
# from player import Player
# from player1 import Player1
# from player2 import Player2
# from player3 import Player3

from random import randrange

import copy

def getWinningTeam(gamestate):
	if gamestate.getWinner()!=None:
		return gamestate.getWinner()
	validMoves = gamestate.getLegalMoves()
	teamToMove = gamestate.getTeamToMove()
	for move in validMoves:
		#Create an independent copy of the gamestate
		newGamestate = copy.deepcopy(gamestate)
		newGamestate.doMove(move)
		if getWinningTeam(newGamestate)==teamToMove:
			return teamToMove
	return gamestate.getOtherTeam(teamToMove)

def main():
	# gamestate = Gamestate(2,1,["9s","Ah"],["Js","Qh"],["Tc","Qc"],["Qd","Jc"],[],[],"Soud","s")
	# gamestate = Gamestate(2,1,["Ah"],["Js","Qh"],["Tc","Qc"],["Qd","Jc"],["9s"],[],"Wes","s")
	gamestate = Gamestate(2,1,["9s"],["Js","Qh"],["Tc","Qc"],["Qd","Jc"],["Ah"],[],"Wes","s")

	print(getWinningTeam(gamestate))


if __name__== "__main__":
	main()

# if __name__ == "__main__":#This is where you decided which player gets what AI
# 	"Test Game"
# 	p1 = Player3("Henry")
# 	p3 = Player3("Paul")
# 	#set local strategies
# 	p1.callPointsForVoidOff = True
# 	p3.callPointsForVoidOff = True
#
# 	p2 = Player3("Alex")
# 	p4 = Player3("Sarah")
#
# 	"Control Game"
# 	p1a = Player3("HenryA")
# 	p3a = Player3("PaulA")
#
# 	p2a = Player3("AlexA")
# 	p4a = Player3("SarahA")
#
# 	team1Score = 0
# 	team1aScore = 0
#
# 	numGames = 1#Number of games played
# 	neededScore = 1#Number of points needed to win a game
# 	printOutput = True#Whether or not each hand is printed in the console
#
# 	for index in range(numGames):
# 		randSeed = randrange(-10000,10000)
#
# 		gTest = Game([p1, p2, p3, p4])
# 		team1Score+=gTest.play_game(neededScore, randSeed, printOutput)
#
# 		gControl = Game([p1a, p2a, p3a, p4a])
# 		team1aScore+=gControl.play_game(neededScore, randSeed, printOutput)
#
# 	print "team 1 won ",team1Score," games out of ", numGames
# 	print "team 1a won ",team1aScore," games out of ", numGames