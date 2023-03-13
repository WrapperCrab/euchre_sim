from random import shuffle, seed, randrange
import utils
import copy

SUITS = ['s', 'h', 'd', 'c']
VALUES = ['9', 'T', 'J', 'Q', 'K', 'A']

class Game:
	def __init__(self, players):
		if len(players) != 4:
			raise IllegalPlayException("Game only supports 5 players")#Don't understand this error
		self._players = players#Always kept the same
		self.dealerIndex=3 #index of dealer in _players
		self.playersOrder = copy.copy(self._players)#shallow copy of players that can be rotated

		# set positions and teams
		self._positions = {}
		self._teams = {}
		self._hands = {p: [] for p in self.playersOrder}
		self._inactives = [] # current inactive player for the hand ("alone")
		position = 0
		for p in self.playersOrder:
			p.game = self

			# set both player attr and position dict for security
			self._positions[p] = position
			p.position = position
			if p.position % 2 == 0:
				p.team_num = 1
				self._teams[p] = 1
			else:
				p.team_num = 2
				self._teams[p] = 2
			position += 1

		self._game_score = {1: 0, 2: 0}
		self._tricks_score = {1: 0, 2: 0}
		self.__deck = None
		self._top_card = None
		self._trump = None
		self._caller = None
		self._dealer = None

	def play_game(self, neededScore, randSeed, printOutput):
		seed(randSeed)
		#Select a random dealer
		self.dealerIndex = randrange(4)
		print(self.dealerIndex)

		while (self._game_score[1] < neededScore and self._game_score[2] < neededScore):
			self.dealerIndex = (self.dealerIndex+1)%4#Go to the next dealer
			self.play_hand(printOutput)
			if printOutput:
				print "===============> SCORE:", self._game_score
		if printOutput:
			print "GAME OVER!"

		#In order to keep track of who's won and lost
		if self._game_score[1]>=neededScore:
			return 1
		return 0

	def play_hand(self, printOutput):
		self._rotate_until_dealer(self.dealerIndex)

		# dealer is the "last" player in order
		self._dealer = self.playersOrder[3]

		# deal
		self.deal_hand()

		# call trump
		self.call_trump(printOutput)
		if printOutput:
			self.print_hand()
		if printOutput:
			print "top card", self._top_card

		# play tricks
		for _ in xrange(5):
			trick = []

			for p in self.playersOrder:
				card = p.action(trick)
				if p not in self._inactives:
					if len(trick) > 0 and p.has_suit(utils.getCardSuit(trick[0],self._trump), self._trump) and (utils.getCardSuit(trick[0],self._trump)!=utils.getCardSuit(card,self._trump)):
						if printOutput:
							print(trick)#!!!This is before the card is added to the trick
							print(card)
						raise IllegalPlayException("Must play the lead suit if you've got it")
					if card not in self._hands[p]:
						raise IllegalPlayException("Player doesn't have that card to play")
					trick.append(card)
					self._hands[p].remove(card) # Game

			winning_card = utils.best_card(trick, self._trump, utils.getCardSuit(trick[0],self._trump))
			winning_player = self.playersOrder[trick.index(winning_card)]
			self._tricks_score[self._teams[winning_player]] += 1

			self._rotate_until_first(winning_player)#!!!This is incorrect anyway
			if printOutput:
				print winning_player.name, winning_card, trick

		# score
		self.score_hand()

		# reset
		self._trump = None
		self._top_card = None
		self._inactives = []
		for team_num in xrange(1, 3):
			self._tricks_score[team_num] = 0
		for p in self.playersOrder:
			self._hands[p] = [] # Game
			p.active = True

	def deal_hand(self):
		self.__deck = [val + suit for val in VALUES for suit in SUITS]
		shuffle(self.__deck)

		#Deal~3232 2323
		parityDeal = 0
		for p in self.playersOrder:
			cardsToDeal = 0
			if parityDeal%2==0:
				cardsToDeal = 3
			else:
				cardsToDeal = 2
			parityDeal+=1
			for _ in xrange(cardsToDeal):
				card = self.__deck.pop()
				self._hands[p].append(card)

		# euchre style dealing, for true authenticity
		#What the fuck you talkin about my man? You'd get beat up if you dealt like this
		# for p in self.playersOrder:
		# 	for _ in xrange(randrange(1,5)):
		# 		card = self.__deck.pop()
		# 		self._hands[p].append(card) # Game

		for p in self.playersOrder:
			for _ in xrange(5-len(self._hands[p])):
				card = self.__deck.pop()
				self._hands[p].append(card) # Game

		self._top_card = self.__deck.pop()

	def call_trump(self, printOutput):
		for p in self.playersOrder:
			call_result = p.call(self._top_card)
			if call_result != False:
				self._trump = self._top_card[1]

				self._hands[self._dealer].append(self._top_card) # Game
				discard = self._dealer.discard()
				self._hands[self._dealer].remove(discard) # Game

				if call_result == "alone":
					self._inactives.append(self._teammate_for(p))
					self._teammate_for(p).active = False
					if self.playersOrder[0]==self._teammate_for(p):
						#The afk is first. rotate
						self.rotate()
						#This implements left of the dealer

				# tell players and game who called
				self._caller = p
				for pl in self.playersOrder:
					pl.end_call(self._positions[p], self._trump)
				return
			if printOutput:
				print p.name, ":", self._trump
		if printOutput:
			self.print_hand()

		for p in self.playersOrder:
			call_result = p.call2(self._top_card)

			if call_result not in SUITS and p == self._dealer:
				raise IllegalPlayException("The dealer got screwed - You have to call something!")
			if call_result == self._top_card[1]:
				if printOutput:
					print(call_result)
					print(self._top_card[1])
				raise IllegalPlayException("Can't call the face up card after it's flipped")
			if call_result in SUITS:
				self._trump = call_result

				# tell players and game who called
				self._caller = p
				for pl in self.playersOrder:
					pl.end_call(self._positions[p], self._trump)
				return

	def score_hand(self):
		calling_team = self._teams[self._caller]
		non_calling_team = (calling_team % 2) + 1
		if self._tricks_score[calling_team] > self._tricks_score[non_calling_team]:
			if self._tricks_score[calling_team] == 5:
				if (self.playersOrder[calling_team-1] in self._inactives) | (self.playersOrder[calling_team+1] in self._inactives):#The winning team went alone!
					#This piece of the code was beyond fucked when I first got to it
					print("this should not have happened")
					self._game_score[calling_team] += 4
				else:
					self._game_score[calling_team] += 2
			else:
				self._game_score[calling_team] += 1
		else:
			self._game_score[non_calling_team] += 2

	def print_hand(self):
		""" Print hand for each player """
		print "------------------- Trump:", self._trump, "---------------"
		for p in self.playersOrder:
			if p not in self._inactives:
				print self._positions[p], p.name, self._hands[p]
			else:
				print self._positions[p], p.name, "*** asleep ***"

	def _teammate_for(self, thisPlayer):
		""" Return teammate of player """
		for index in range(4):
			if (self.playersOrder[index] == thisPlayer):
				return self.playersOrder[(index+2)%4]

	def _rotate(self):
		""" Rotate players in self.playersOrder so that player after dealer becomes dealer """
		self.playersOrder = self.playersOrder[1:] + self.playersOrder[:1]#!!!This should work, but it's acting funky

	def _rotate_until_dealer(self, dealerIndex):
		""" Rotate players in self.playersOrder until dealer is in the dealer position again"""
		print(dealerIndex)
		while self.playersOrder[3] != self._players[dealerIndex]:
			self._rotate()

	def _rotate_until_first(self, winner):
		#winner refers to a player in playersOrder
		while self.playersOrder[0] != winner:
			self._rotate()

	def hand_for(self, player):
		""" Return hand of specified player """
		return self._hands[player]

	def position_for(self, player):
		""" Return position of specified player """
		return self._positions[player]

	def team_num_for(self, player):
		""" Return team_num of specified player """
		if player in self._teams[1]:
			return 1
		elif player in self._teams[2]:
			return 2
		else:
			raise Exception("You don't appear to be on either team :/")

	def is_player_active(self, player):
		""" Return True if player is active this hand """
		return player not in self._inactives

	@property
	def top_card(self):
		return self._top_card

	@property
	def trump(self):
		return self._trump

	@property
	def caller_pos(self):
		return self._positions[self._caller]

	@property
	def dealer_pos(self):
		return self._positions[self._dealer]

	@property
	def tricks_score(self):
		return self._tricks_score

	@property
	def game_score(self):
		return self._game_score

class IllegalPlayException(Exception):
	pass
