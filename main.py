import utils
from game import Game

import copy
# from player import Player
# from player1 import Player1
# from player2 import Player2
# from player3 import Player3

import copy
from random import shuffle
from gamestate import Gamestate

from random import randrange


SUITS = ['s', 'h', 'd', 'c']
VALUES = ['9', 'T', 'J', 'Q', 'K', 'A']

def getRandomCards(deck,numCards):
	newDeck = copy.copy(deck)
	shuffle(newDeck)
	cardsToReturn = []
	for index in range(numCards):
		cardsToReturn.append(newDeck.pop())
	return cardsToReturn

def getDeckMinusCards(cards):
	#returns an array with the rest of the deck excluding cards
	deck = [val + suit for val in VALUES for suit in SUITS]
	for card in cards:
		deck.remove(card)
	return deck

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
		else:
			continue
	return gamestate.getOtherTeam(teamToMove)

def main():
	aceWins = 0
	nineWins = 0

	remainingDeck = getDeckMinusCards(["9s","Ah"])
	for i in range(100):#play the Ah
		newCards = getRandomCards(remainingDeck,6)
		wHand = newCards[:2]
		nHand = newCards[2:4]
		eHand = newCards[4:]
		gamestate = Gamestate(2,1,["9s"],wHand,nHand,eHand,["Ah"],[],"Wes","s")
		if getWinningTeam(gamestate)=="NS":
			aceWins+=1
	for i in range(100):#play the Ah
		newCards = getRandomCards(remainingDeck,6)
		wHand = newCards[:2]
		nHand = newCards[2:4]
		eHand = newCards[4:]
		gamestate = Gamestate(2,1,["Ah"],wHand,nHand,eHand,["9s"],[],"Wes","s")
		if getWinningTeam(gamestate)=="NS":
			nineWins+=1

	print("Ace of hearts won: " + str(aceWins) + " times")
	print("9 of spades won: " + str(nineWins) + " times")


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