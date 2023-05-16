import utils

class Player:

	def __init__(self, name):
		self.name = name
		self.game = None

	def action(self, trick, playersInTrick):#The original function didn't know that the left changes suit. Pathetic.
		""" Play a card in trick
		trick -- list of cards played in order, trick[0] is lead card
		playersInTrick -- list of players that played the corresponding card in trick
		"""
		if len(trick) == 0:
			#we are first
			return self.game.hand_for(self)[0]#first card in hand
		else:#We are not first, there is a led suit
			ledSuit = utils.getCardSuit(trick[0],self.game.trump)
			for card in self.game.hand_for(self):
				cardSuit = utils.getCardSuit(card,self.game.trump)
				if (cardSuit == ledSuit):
					#this is the same suit as the lead suit
					return card
			#We only get here if we have no lead suit
			return self.game.hand_for(self)[0]

	def call(self, top_card):
		""" Call trump or pass

		If top_card is specified return:
			True - call the top_card suit as trump
			"alone" - call that suit trump, and put partner to sleep / go alone
			False - pass
		"""
		return True#always call (lol)

	def call2(self, top_card):
		"""this is run when all players passed in first round"""
		"""return [suit,True/False/"alone"]"""
		if top_card[1]=='d':
			return ['s',True]
		return ['d',"alone"]

	def discard(self):
		""" Choose card to discard after picking up
		Return the string (like 'As' or 'Th'), it will automatically be removed from hand
		"""
		return self.game.hand_for(self)[0]

	def end_trick(self, winner_position, lead_position, trick):
		#I don't see the purpose of this function
		""" Communicate result of trick to player
		winner_position - position of winner of trick
		lead_position - position of player who led trick, used to tell who played what
		"""
		pass

	def endCall1(self,trumpDecided,callPosition,goingAlone):
		#called when the first round of calls ends. All relevant info is within parameters of this call
		pass

	def endCall2(self,callPosition,goingAlone):
		#called when the second round of calls ends
		pass

	def endTrick(self,winPosition,trick):
		#called when a trick ends
		pass

	def endRound(self):
		#called when a round ends
		#idea is to use this to reset variables
		pass

	def has_suit(self, suit, trump):#the original function did not consider the left. I'm sensing a pattern
		""" Return True if player has specified suit in hand, otherwise false """
		for card in self.game.hand_for(self):
			if utils.getCardSuit(card,trump)==suit:
				return True
		return False
