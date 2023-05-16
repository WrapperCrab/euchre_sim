import utils
from player import Player

class Player1(Player):
	#local strategies
	numTrumpToCall = 3

	def call(self, top_card):
		""" Call trump or pass """
		numMatch = 0
		for card in self.game.hand_for(self):
			if utils.getCardSuit(card,top_card[1]) == top_card[1]:
				numMatch+=1
		position = self.game.get_player_position(self)
		if position==3:#we are the dealer
			numMatch+=1
		if numMatch >= self.numTrumpToCall:
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
		if (hCount>=self.numTrumpToCall) & (bannedSuit!='h'):
			return ["h",True]
		elif (sCount>=self.numTrumpToCall) & (bannedSuit!='s'):
			return ["s",True]
		elif (cCount>=self.numTrumpToCall) & (bannedSuit!='c'):
			return ["c",True]
		elif (dCount>=self.numTrumpToCall) & (bannedSuit!='d'):
			return ["d",True]
		elif self.game.get_player_position(self)!=3:#We are not the dealer
			return [None,False]
		else:
			if bannedSuit!='h':
				return ["h",True]
			else:
				return ["s",True]

	def discard(self):
		""" Choose card to discard after picking up	"""
		for card in self.game.hand_for(self):
			if utils.getCardSuit(card,self.game.trump)!=self.game.trump:
				return card
		return self.game.hand_for(self)[0]#we have only trump

	def action(self, trick, playersInTrick):
		""" Play a card in trick """
		card_to_play = None
		trumpSuit = self.game.trump
		cards = self.game.hand_for(self)

		if len(trick)==0:#we are first
			#find highest card overall
			card_to_play = utils.best_card(self.game.hand_for(self), trumpSuit, None)
		else:#we are not first
			ledSuit = utils.getCardSuit(trick[0],trumpSuit)
			legalCards = utils.getLegalCards(cards,trumpSuit,ledSuit)
			card_to_play = utils.best_card(legalCards, trumpSuit, ledSuit)
		return card_to_play