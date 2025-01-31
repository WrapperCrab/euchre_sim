import utils
from player2 import Player2

class PlayerUnfinished(Player2):
	def call(self, top_card):
		""" Call trump or pass """
		#calling is drastically different depending on your position at the table
		#!!!position = self.game.position_for(self)
		#unfortunately, this function does not return what it should. It is constant for the whole game
		#This works instead
		position = 0
		for index in range(4):
			if self.game.playersOrder[index] == self:
				position = index


		myHand = self.game.hand_for(self)
		cp = 0
		wouldBeTrump = top_card[1]

		if position == 0:
			if utils.best_card(myHand.append(top_card), wouldBeTrump,None)==top_card:
				cp +=-1
		elif position == 1:
			if top_card[0]=='J':
				cp+=.7
			elif top_card[0]=='A':
				cp+=.2
		elif position == 2:
			if utils.best_card(myHand.append(top_card), wouldBeTrump,None)==top_card:
				cp +=-1
		else: #(position==3)
			myHand = myHand.append(top_card).remove(discard())

		myTrumpCards = getLegalCards(myHand, wouldBeTrump, wouldBeTrump)
		numTrump = len(myTrumpCards)
		if numTrump ==0:
			cp +=-1
		elif numTrump==1:
			cp +=-.5
		elif numTrump==2:
			cp+=0
		elif numTrump==3:
			cp+=.3
		elif numTrump==4:
			cp+=.6
		else:#All is trump
			cp+=1

		for card in myTrumpCards:
			if (card[0]=='J') & (card[1]==wouldBeTrump):#this is the right
				cp+=1
			elif card[0]=='J':#This is the left
				cp+=.5
			elif card[0]=='A':
				cp+=.2

		if numTrump!=0:
			hasHearts = False
			hasDiamonds = False
			hasSpades = False
			hasClubs = False
			for card in myHand:
				if utils.getCardSuit(card)=='h':
					hasHearts=True
				elif utils.getCardSuit(card)=='d':
					hasDiamonds = True
				elif utils.getCardSuit(card)=='s':
					hasSpades = True
				else:
					hasClubs = True
			if (hasHearts==False)|(hasDiamonds==False)|(hasSpades==False)|(hasClubs==False):
				cp+=.3

		if cp>=2.5:
			return True
		elif cp>=4:
			return "alone"

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
		return worstCard(self.game.hand_for(self), self.game.trump, None)

