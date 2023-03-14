import utils
from player1 import Player1

class Player1B(Player1):
	def call(self, top_card):
		""" Call trump or pass """
		numMatch = 0
		for card in self.game.hand_for(self):
			if utils.getCardSuit(card,top_card[1]) == top_card[1]:
				numMatch+=1
		position = self.game.get_player_position(self)
		if position==3:#we are the dealer
			numMatch+=1
		if numMatch >= 3:
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
			return ["h",True]
		elif (sCount>=3) & (bannedSuit!='s'):
			return ["s",True]
		elif (cCount>=3) & (bannedSuit!='c'):
			return ["c",True]
		elif (dCount>=3) & (bannedSuit!='d'):
			return ["d",True]
		elif self.game.get_player_position(self)!=3:#We are not the dealer
			return [None,False]
		else:
			if bannedSuit!='h':
				return ["h",True]
			else:
				return ["s",True]
