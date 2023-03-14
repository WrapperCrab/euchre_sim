from random import shuffle, seed, randrange
import utils
import copy

SUITS = ['s', 'h', 'd', 'c']
VALUES = ['9', 'T', 'J', 'Q', 'K', 'A']

class Game:
	def __init__(self, players):
		if len(players) != 4:
			raise IllegalPlayException("Game only supports 4 players")
		self._players = players#Always kept the same
		self.dealerIndex=3 #index of dealer in _players
		self.playersOrder = copy.copy(self._players)#shallow copy of players that can be rotated

		# set positions and teams
		self._teams = [[], []]
		self._hands = {p: [] for p in self.playersOrder}
		self._inactives = [] # current inactive player for the hand ("alone")
		for p in self.playersOrder:
			p.game = self
			if p == self.playersOrder[0] or p== self.playersOrder[2]:
				p.team_num = 1
				self._teams[0].append(p)
			else:
				p.team_num = 2
				self._teams[1].append(p)

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

		# play tricks
		for _ in xrange(5):
			trick = []
			playersInTrick = []
			for index in range(4):
				p = self.playersOrder[index]
				if p not in self._inactives:
					card = p.action(trick)

					leadSuit = None
					if len(trick)>0:
						leadSuit = utils.getCardSuit(trick[0],self._trump)
					playedSuit = utils.getCardSuit(card,self._trump)
					if len(trick) > 0 and p.has_suit(leadSuit, self._trump) and leadSuit!=playedSuit:
						raise IllegalPlayException("Must play the lead suit if you've got it")
					if card not in self._hands[p]:
						raise IllegalPlayException("Player doesn't have that card to play")
					trick.append(card)
					playersInTrick.append(p)
					self._hands[p].remove(card) # Game

			winning_card = utils.best_card(trick, self._trump, utils.getCardSuit(trick[0],self._trump))
			winning_player = playersInTrick[trick.index(winning_card)]
			self._tricks_score[self.team_num_for(winning_player)] += 1

			self._rotate_until_first(winning_player)
			if printOutput:
				print winning_player.name, winning_card, trick

		# score
		self.score_hand()

		# reset
		self._trump = None
		self._top_card = None
		self._inactives = []
		self._dealer = None
		self._caller = None
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
		for index in range(4):
			p=self.playersOrder[index]
			cardsToDeal = 0
			if parityDeal%2==0:
				cardsToDeal = 3
			else:
				cardsToDeal = 2
			parityDeal+=1
			for _ in xrange(cardsToDeal):
				card = self.__deck.pop()
				self._hands[p].append(card)

		for index in range(4):
			p=self.playersOrder[index]
			for _ in xrange(5-len(self._hands[p])):
				card = self.__deck.pop()
				self._hands[p].append(card) # Game

		self._top_card = self.__deck.pop()

	def call_trump(self, printOutput):
		if printOutput:
			print "top card", self._top_card
		for index in range(4):
			p=self.playersOrder[index]
			call_result = p.call(self._top_card)
			if call_result != False:
				#The suit has been called
				self._trump = self._top_card[1]
				self._hands[self._dealer].append(self._top_card) # Game
				discard = self._dealer.discard()
				self._hands[self._dealer].remove(discard) # Game

				if call_result == "alone":
					#this is redundant
					self._inactives.append(self._teammate_for(p))
					self._teammate_for(p).active = False
					if self.playersOrder[0]==self._teammate_for(p):
						#The afk is first. rotate
						self._rotate()
						#This implements left of the dealer
					if printOutput:
						print p.name, ":", self._trump, "  Alone!"
				else:
					if printOutput:
						print p.name, ":", self._trump

				# tell players and game who called
				self._caller = p
				return
			if printOutput:
				print p.name, ":" , self._trump

		print "top card flipped over"
		#second pass
		for index in range(4):
			p=self.playersOrder[index]
			call = p.call2(self._top_card)
			if call[1] == False:
				#they passed
				if p==self._dealer:
					raise IllegalPlayException("The dealer got screwed - You have to call something!")
				#This is a legal pass
				if printOutput:
					print p.name, ":", self._trump
			else:
				#they did not pass
				call_result = call[0]
				if call_result == self._top_card[1]:
					raise IllegalPlayException("Can't call the face up card after it's flipped")
				self._trump = call_result
				self._caller = p
				if call[1] == "alone":
					#They went alone
					#this is redundant
					self._inactives.append(self._teammate_for(p))
					self._teammate_for(p).active = False
					if self.playersOrder[0]==self._teammate_for(p):
						#The afk is first. rotate
						self._rotate()
						#This implements left of the dealer
					if printOutput:
						print p.name, ":", self._trump, "  Alone!"
				else:
					#The did not go alone
					if printOutput:
						print p.name, ":", self._trump
				return

	def score_hand(self):
		calling_team_num = self.team_num_for(self._caller)
		non_calling_team_num = (calling_team_num%2)+1
		calling_team = self._teams[calling_team_num-1]
		non_calling_team = self._teams[non_calling_team_num-1]
		if self._tricks_score[calling_team_num] > self._tricks_score[non_calling_team_num]:
			#calling team won
			if self._tricks_score[calling_team_num] == 5:
				#calling team got all 5
				if (calling_team[0] in self._inactives) | (calling_team[1] in self._inactives):
					#calling team went alone
					self._game_score[calling_team_num] += 4
				else:
					#calling team did not go alone
					self._game_score[calling_team_num] += 2
			else:
				#calling team did not get all 5
				self._game_score[calling_team_num] += 1
		else:
			#calling team lost
			self._game_score[non_calling_team_num] += 2

	def print_hand(self):
		""" Print hand for each player """
		print "------------------- Trump:", self._trump, "---------------"
		for index in range(4):
			p=self.playersOrder[index]

			if p not in self._inactives:
				print self.get_player_position(p), p.name, self._hands[p]
			else:
				print self.get_player_position(p), p.name, "*** asleep ***"

	def _teammate_for(self, thisPlayer):
		""" Return teammate of player """
		for index in range(4):
			if (self.playersOrder[index] == thisPlayer):
				return self.playersOrder[(index+2)%4]

	def _rotate(self):
		""" Rotate players in self.playersOrder so that player after dealer becomes dealer """
		self.playersOrder = self.playersOrder[1:] + self.playersOrder[:1]

	def _rotate_until_dealer(self, dealerIndex):
		""" Rotate players in self.playersOrder until dealer is in the dealer position again"""
		while self.playersOrder[3] != self._players[dealerIndex]:
			self._rotate()

	def _rotate_until_first(self, winner):
		#winner refers to a player in playersOrder
		while self.playersOrder[0] != winner:
			self._rotate()

	def hand_for(self, player):
		""" Return hand of specified player """
		return self._hands[player]

	def team_num_for(self, player):
		""" Return team_num of specified player """
		if player in self._teams[0]:
			return 1
		elif player in self._teams[1]:
			return 2
		else:
			raise Exception("You don't appear to be on either team :/")

	def is_player_active(self, player):
		""" Return True if player is active this hand """
		return player not in self._inactives

	def get_player_position(self,player):
		playerIndex = 0
		for index in range(4):
			if self._players[index]==player:
				playerIndex = index
				break
		return ((3+(playerIndex-self.dealerIndex))%4)




	@property
	def top_card(self):
		return self._top_card

	@property
	def trump(self):
		return self._trump

	@property
	def tricks_score(self):
		return self._tricks_score

	@property
	def game_score(self):
		return self._game_score

class IllegalPlayException(Exception):
	pass
