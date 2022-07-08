import utils
from player import Player

class Player2(Player):

	def __init__(self, name):
		Player.__init__(self, name)

	def action(self, trick):
		""" Play a card in trick """
		card_to_play = None
		trumpSuit = self.game.trump
		myHand = self.game.hand_for(self)

		if not trick:#we are first
			#find highest card overall
			card_to_play = utils.best_card(myHand, trumpSuit, None)
		else:#we are not first
			leadSuit = utils.getCardSuit(trick[0],trumpSuit)
			myPlays = utils.getLegalCards(myHand, trumpSuit, leadSuit)
			if utils.myTeamIsWinning(trick, trumpSuit):#Our team is winning
				card_to_play = utils.worstCard(myPlays, trumpSuit, leadSuit)
			else:#Our team is losing
				cardToBeat = utils.best_card(trick, trumpSuit, leadSuit)
				myPlaysThatWin = []
				for card in myPlays:
					if utils.best_card([card, cardToBeat], trumpSuit, leadSuit)==card:
						myPlaysThatWin.append(card)
				if not myPlaysThatWin:#We cannot win
					card_to_play = utils.worstCard(myPlays, trumpSuit, leadSuit)
				else:#We can win
					card_to_play = utils.worstCard(myPlaysThatWin, trumpSuit, leadSuit)
		return card_to_play

def call(self, top_card):
	""" Call trump or pass """
	numMatch = 0
	for card in self.game.hand_for(self):
		if utils.getCardSuit(card,top_card[1]) == top_card[1]:
			numMatch+=1
	if numMatch >= 2:
		return True
	return False

def call2(self, top_card):
	bannedSuit = top_card[1]
	hCount = 0
	sCount = 0
	cCount = 0
	dCount = 0
	for card in self.game.hand_for(self):
		if utils.getCardSuit(card,'h')=="h":
			hCount+=1
		if utils.getCardSuit(card,'s')=="s":
			sCount+=1
		if utils.getCardSuit(card,'c')=="c":
			cCount+=1
		if utils.getCardSuit(card,'d')=="d":
			dCount+=1
	if (hCount>=3) & (bannedSuit!='h'):
		return "h"
	elif (sCount>=3) & (bannedSuit!='s'):
		return "s"
	elif (cCount>=3) & (bannedSuit!='c'):
		return "c"
	elif (dCount>=3) & (bannedSuit!='d'):
		return "d"
	elif self.game.position_for(self)!=3:#We are not the dealer
		return False
	else:
		if bannedSuit!='h':
			return "h"
		else:
			return "s"

	def discard(self):
		""" Choose card to discard after picking up	"""
		for card in self.game.hand_for(self):
			if utils.getCardSuit(card,self.game.trump)!=self.game.trump:
				return card
		return self.game.hand_for(self)[0]#we have only trump

	def end_call(self, caller_position, trump):
		""" Communicate result of calling to player """
		pass

	def end_trick(self):
		""" Communicate result of trick to player """
		pass
