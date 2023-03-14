import utils
from player import Player

class Player1(Player):
	def call(self, top_card):
		""" Call trump or pass """
		numMatch = 0
		for card in self.game.hand_for(self):
			if utils.getCardSuit(card,top_card[1]) == top_card[1]:
				numMatch+=1
		position = self.game.get_player_position(self)
		if position==3:#we are the dealer
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
		if (hCount>=2) & (bannedSuit!='h'):
			return ["h",True]
		elif (sCount>=2) & (bannedSuit!='s'):
			return ["s",True]
		elif (cCount>=2) & (bannedSuit!='c'):
			return ["c",True]
		elif (dCount>=2) & (bannedSuit!='d'):
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

		if len(trick)==0:#we are first
			#find highest card overall
			card_to_play = utils.best_card(self.game.hand_for(self), trumpSuit, None)
		else:#we are not first
			ledSuit = utils.getCardSuit(trick[0],trumpSuit)
			ledSuitCards = []
			for card in self.game.hand_for(self):
				if utils.getCardSuit(card,trumpSuit) == ledSuit:
					ledSuitCards.append(card) #add this card

			if len(ledSuitCards)==0:
				card_to_play = utils.best_card(self.game.hand_for(self), trumpSuit, ledSuit)
			else:
				card_to_play = utils.best_card(ledSuitCards, trumpSuit, ledSuit)
		return card_to_play