import utils
from player1 import Player1

class Player2(Player1):
	#local strategy bools
	callToLead = True
	shakeTheTree = True
	splitTheTrump = True
	voidAtLoss = True
	voidAtStart = True


	def action(self, trick, playersInTrick):
		#Play a card in trick
		if len(trick)==0:#we are first
			return self.lead()
		else:#we are not first
			return self.follow(trick,playersInTrick)

	def lead(self):
		card_to_play = None
		trumpSuit = self.game.trump
		myHand = self.game.hand_for(self)

		if self.callToLead:
			if (utils.hasCard(myHand,'J',trumpSuit))and(self.weCalled):#should keep track of what is best remaining card
				card_to_play = 'J'+trumpSuit
				return card_to_play

		if self.shakeTheTree:
			if (len(myHand)==5)and(not utils.hasCard(myHand,'J',trumpSuit))and(self.weCalled):
				trumpCards = utils.getCardsOfSuit(myHand,trumpSuit,trumpSuit)
				if len(trumpCards)>0:
					card_to_play = utils.worstCard(trumpCards,trumpSuit,None)
					if (card_to_play[0]!='J') and (card_to_play[0]!='A'):
						return card_to_play

		if self.splitTheTrump:
			if (len(myHand) == 5) and (not self.weCalled):
				nonTrumpCards = utils.getCardsNotOfSuit(myHand,trumpSuit,trumpSuit)
				if len(nonTrumpCards)!=0:
					card_to_play = utils.best_card(nonTrumpCards,trumpSuit,None)
					return card_to_play

		if self.voidAtStart:
			if (utils.hasSuit(myHand,trumpSuit,trumpSuit)):
				#Try to void
				cardsThatVoid = utils.getCardsThatVoid(myHand, trumpSuit)
				if len(cardsThatVoid) > 0:
					card_to_play = utils.worstCard(cardsThatVoid, trumpSuit, None)
					return card_to_play

		#base strategy
		# find highest card overall
		card_to_play = utils.best_card(myHand, trumpSuit, None)
		return card_to_play

	def follow(self,trick,playersInTrick):
		card_to_play = None
		trumpSuit = self.game.trump
		myHand = self.game.hand_for(self)

		ledSuit = utils.getCardSuit(trick[0], trumpSuit)
		myPlays = utils.getLegalCards(myHand, trumpSuit, ledSuit)
		team = self.game._teams[self.game.team_num_for(self) - 1]
		if utils.myTeamIsWinning(trick, playersInTrick, team, trumpSuit):  # Our team is winning
			card_to_play = utils.worstCard(myPlays, trumpSuit, ledSuit)
		else:  # Our team is losing
			cardToBeat = utils.best_card(trick, trumpSuit, ledSuit)
			myPlaysThatWin = []
			for card in myPlays:
				if utils.best_card([card, cardToBeat], trumpSuit, ledSuit) == card:
					myPlaysThatWin.append(card)
			if not myPlaysThatWin:  # We cannot win

				if self.voidAtLoss:
					if (len(myPlays) == len(myHand)) and (utils.hasSuit(myPlays,trumpSuit,trumpSuit)):
						cardsThatVoid = utils.getCardsThatVoid(myHand,trumpSuit)
						if len(cardsThatVoid)>0:
							card_to_play = utils.worstCard(cardsThatVoid,trumpSuit,ledSuit)
							return card_to_play


				card_to_play = utils.worstCard(myPlays, trumpSuit, ledSuit)
			else:  # We can win
				card_to_play = utils.worstCard(myPlaysThatWin, trumpSuit, ledSuit)
		return card_to_play

	def endCall1(self, trumpDecided, callPosition,goingAlone):
		# called when the first round of calls ends. All relevant info is within parameters of this call
		if (self.callToLead) or (self.shakeTheTree) or (self.splitTheTrump):
			#This always happens when callToLead is true
			self.weCalled = False
			if trumpDecided:
				myPosition = self.game.get_player_position(self)
				teammatePosition = (myPosition+2)%4
				if (callPosition==myPosition) or (callPosition==teammatePosition):
					self.weCalled = True

	def endCall2(self, callPosition,goingAlone):
		# called when the second round of calls ends
		if (self.callToLead) or (self.shakeTheTree) or (self.splitTheTrump):
			myPosition = self.game.get_player_position(self)
			teammatePosition = (myPosition+2)%4
			if (callPosition==myPosition) or (callPosition==teammatePosition):
				self.weCalled = True

	def endRound(self):
		if (self.callToLead) or (self.shakeTheTree) or (self.splitTheTrump):
			self.weCalled = False