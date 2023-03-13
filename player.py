import utils

class Player:

	def __init__(self, name):
		self.name = name
		self.game = None

	def action(self, trick):#The original function didn't know that the left changes suit. Pathetic.
		""" Play a card in trick

		trick -- list of cards played in order, trick[0] is lead card

		"""
		if not trick:#if we are first
			return self.game.hand_for(self)[0]#first card in hand
		else:#We are not first, there is a lead suit
			for card in self.game.hand_for(self):
				if (utils.getCardSuit(card,self.game.trump) == utils.getCardSuit(trick[0],self.game.trump)):
					#this is the same suit as the lead suit
					return card
			#We only get here if we have no lead suit
			return self.game.hand_for(self)[0]

		# for card in self.game.hand_for(self):#!!!I don't think this for loop makes much sense here
		# 	if not trick:#I think, this is saying if we are first
		# 		card_to_play = self.game.hand_for(self)[0]#first card in hand
		# 	elif trick[0][1] == card[1]:#card[1] is the suit of the play we are considering.
		# 		card_to_play = card# If it is the same, play it
		# if not card_to_play:#if card_to_play is not decided yet, AKA if we are not first and don't have the suit of the lead card
		# 	card_to_play = self.game.hand_for(self)[0]#first card in hand
		# return card_to_play

	def call(self, top_card):
		""" Call trump or pass

		If top_card is specified return:
			True - call the top_card suit as trump
			"alone" - call that suit trump, and put partner to sleep / go alone
			False - pass

		If top_card is None, return:
			's', 'c', 'h', 'd' - call specified suit as trump
			False - pass
			*** note if player is dealer (position == 3), player can't pass

		"""
		#return True#always call (lol)
		#if in position 3, go alone
		position = 0
		for index in range(4):
			if self.game.playersOrder[index] == self:
				position = index

		if position==3:
			return "alone"

		#else, pass
		return "alone"

	def call2(self, top_card):
		"""this is run when all players passed in first round"""
		pass

	def discard(self):
		""" Choose card to discard after picking up

		Return the string (like 'As' or 'Th'), it will automatically be removed from hand

		"""
		return self.game.hand_for(self)[0]

	def end_call(self, caller_position, trump):
		""" Communicate result of calling to player

		caller_position -- current position of player who called, so if your position is 0, your
			teammate would be 2
		trump -- the trump that was called.  can also be accessed via self.game.trump

		"""
		pass#placeholder that does nothing, and doesn't throw a compile error

	def end_trick(self, winner_position, lead_position, trick):
		""" Communicate result of trick to player

		winner_position - position of winner of trick
		lead_position - position of player who led trick, used to tell who played what

		"""
		pass

	def has_suit(self, suit, trump):#the original function did not consider the left. I'm sensing a pattern
		""" Return True if player has specified suit in hand, otherwise false """
		for card in self.game.hand_for(self):
			if utils.getCardSuit(card,trump)==suit:
				return True
		return False
			#card[1], the second attribute of card, is the suit
