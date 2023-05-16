import utils
from player1 import Player1

class Player2(Player1):
	#local strategy bools
	callToLead = False
	shakeTheTree = False
	splitTheTrump = False
	voidAtLoss = False

	weCalled = False

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
			if (len(myHand)==5)and(utils.hasCard(myHand,'J',trumpSuit))and(self.weCalled):
				card_to_play = 'J'+trumpSuit
				return card_to_play
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
				card_to_play = utils.worstCard(myPlays, trumpSuit, ledSuit)
			else:  # We can win
				card_to_play = utils.worstCard(myPlaysThatWin, trumpSuit, ledSuit)
		return card_to_play

	def endCall1(self, trumpDecided, callPosition,goingAlone):
		# called when the first round of calls ends. All relevant info is within parameters of this call
		if (self.callToLead):
			#This always happens when callToLead is true
			self.weCalled = False
			if trumpDecided:
				myPosition = self.game.get_player_position(self)
				teammatePosition = (myPosition+2)%4
				if (callPosition==myPosition) or (callPosition==teammatePosition):
					self.weCalled = True

	def endCall2(self, callPosition,goingAlone):
		# called when the second round of calls ends
		if (self.callToLead):
			myPosition = self.game.get_player_position(self)
			teammatePosition = (myPosition+2)%4
			if (callPosition==myPosition) or (callPosition==teammatePosition):
				self.weCalled = True

	def endRound(self):
		if (self.callToLead):
			self.weCalled = False