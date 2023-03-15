import utils

import copy

VALUE_MAP = {'9': 1, 'T': 2, 'J': 3, 'Q': 4, 'K': 5, 'A': 6}

def best_card(cards, trump=None, lead=None):
	""" Calculate winning card from list of cards

	Trump and lead suit must be specified, otherwise normal order is assumed.

	I am displeased with the lack of elegance in this function.

	"""
	val_map = {}
	for c in cards:
		val = VALUE_MAP[c[0]]
		if trump == c[1]:#This is trump, may be right
			if c[0] == 'J':#this is the right
				val += 40
			else:#This is normal trump
				val += 20
		elif (trump == same_color(c[1])) & (c[0] == 'J'):#this is the left
			val +=30
		else:#This is not trump
			if lead == c[1]:#This is lead
				val += 10
			# else:#this card is not special
		val_map[c] = val
	return sorted(val_map.items(), key=lambda x: x[1], reverse=True)[0][0]

def same_color(suit):
	""" Return other suit of the same same color"""
	if suit == 's':
		return 'c'
	elif suit == 'c':
		return 's'
	elif suit == 'd':
		return 'h'
	elif suit == 'h':
		return 'd'

def getCardSuit(card, trump):#I wrote this
	"""return the true suit of the card"""
	if (card[0]=='J') & (card[1]==same_color(trump)):
		return trump#This is the left
	else:
		return card[1]

def getLegalCards(cards, trump, lead):
	legalCards = []
	suitFollowingCards = []
	for card in cards:
		if getCardSuit(card, trump)==lead:
			suitFollowingCards.append(card)
	if not suitFollowingCards:#We have no cards following suit
		legalCards = cards
	else:#WE do have cards following suit
		legalCards = suitFollowingCards
	return legalCards

def myTeamIsWinning(trick, playersInTrick, team,trump):
	if len(trick)==0:
		return True
	elif len(trick)>=1:
		ledSuit = getCardSuit(trick[0], trump)
		winningCard = best_card(trick, trump, ledSuit)
		#find which team this card belongs to
		if len(trick)!=len(playersInTrick):
			print("trick and playersInTrick are different lengths")
		winningPlayer = playersInTrick[trick.index(winningCard)]
		if winningPlayer in team:
			return True
		return False

def worstCard(cards, trump, lead):#I could definitely merge this with best_card, but I don't feel it right now
	#Works even when trump and or lead is None
	val_map = {}
	for c in cards:
		val = VALUE_MAP[c[0]]
		if trump == c[1]:#This is trump, may be right
			if c[0] == 'J':#this is the right
				val += 40
			else:#This is normal trump
				val += 20
		elif (trump == same_color(c[1])) & (c[0] == 'J'):#this is the left
			val +=30
		else:#This is not trump
			if lead == c[1]:#This is lead
				val += 10
			# else:#this card is not special
		val_map[c] = val
	return sorted(val_map.items(), key=lambda x: x[1], reverse=False)[0][0]

def getCardsOfSuit(cards,suit, trump):
	cardsOfSuit = []
	for card in cards:
		if utils.getCardSuit(card,trump)==suit:
			cardsOfSuit.append(card)
	return cardsOfSuit

def getGreenSuits(trump):
	greenSuits = ['d', 'h', 's', 'c']
	greenSuits.remove(trump)
	greenSuits.remove(utils.same_color(trump))
	return greenSuits

def getVoidCard(cards, trump):
	cardsOfTrump = utils.getCardsOfSuit(cards, trump, trump)
	if 0 < len(cardsOfTrump):  # we have trump, look to void in a suit
		greenSuits = utils.getGreenSuits(trump)
		for suit in greenSuits:
			cardsOfSuit = utils.getCardsOfSuit(cards, suit, trump)
			if len(cardsOfSuit) == 1:  # we can void in this suit
				return cardsOfSuit[0]
		otherSuit = utils.same_color(trump)
		cardsOfOtherSuit = utils.getCardsOfSuit(cards, otherSuit, trump)
		if len(cardsOfOtherSuit) == 1:
			return cardsOfOtherSuit[0]
	return None

def hasSuit(cards,trump,suit):
	for card in cards:
		if utils.getCardSuit(card,trump)==suit:
			return True
	return False


def getLikelyOutrides(cards,trump):
	#!!!this function will need to be updated and improved
	# find offsuits that can go all the way through
	outrides = []
	greenSuits = utils.getGreenSuits(trump)
	for suit in greenSuits:
		cardsOfSuit = utils.getCardsOfSuit(cards, suit, trump)
		#!!!this does not take into account how far we are into the round
		if len(cardsOfSuit) > 0:
			if len(cardsOfSuit) <= 3:
				# play the ace
				ace = utils.findCardInCards(cardsOfSuit, 'A', suit)
				if ace != None:
					outrides.append(ace)
			if len(cardsOfSuit) == 1:
				# play the king
				king = utils.findCardInCards(cardsOfSuit, 'K', suit)
				if king != None:
					outrides.append(king)
#			if len(cardsOfSuit) == 1:  # !!!highly doubtful that this is a good idea
#				# play the queen
#				queen = utils.findCardInCards(cardsOfSuit, 'Q', suit)
#				if queen != None:
#					outrides.append(queen)
	otherSuit = utils.same_color(trump)
	cardsOfOther = utils.getCardsOfSuit(cards, otherSuit, trump)
	if len(cardsOfOther) > 0:
		if len(cardsOfOther) <= 2:
			# play the ace
			ace = utils.findCardInCards(cardsOfOther, 'A', otherSuit)
			if ace != None:
				outrides.append(ace)
#		if len(cardsOfOther) == 1:
#			# play the king
#			king = utils.findCardInCards(cardsOfOther, 'K', otherSuit)
#			if king != None:
#				outrides.append(king)
	return outrides

def myTeamIsLikelyToWin(trick,playersInTrick,team,trump,player,caller):
	#!!!must consider strength of partner's card and who all has gone
	#has our partner played yet?
	partner = None
	for person in team:
		if person!=player:
			partner = person
	if partner in playersInTrick:
		#partner has played
		if utils.myTeamIsWinning(trick, playersInTrick, team, trump):
			# we are currently winning
			return True#!!!
		else:
			# we are currently losing
			return False
	else:
		#partner has not played
		ledCard = trick[0]
		if utils.getCardSuit(ledCard,trump)==trump:
			#foe led trump
			if caller==partner:
				#partner called
				return True
			else:
				#partner did not call
				return False
		else:
			if (ledCard[0]=='9') or (ledCard[0]=='T') or (ledCard[0]=='J') or (ledCard[0]=='Q'):
				return True#!!!
			else:
				return False

def getCardsThatAreLikelyToWin(trick,playersInTrick,team,otherTeam,caller,trump,cards):
	ledSuit = utils.getCardSuit(trick[0], trump)
	cardsThatWouldWin = []
	bestCard = utils.best_card(trick)
	for card in cards:
		if card == best_card([card,bestCard], trump, ledSuit):
			cardsThatWouldWin.append(card)
	if len(cardsThatWouldWin) == 0:
		# we cannot win
		return []
	otherTeamStillHasToGo = False
	for person in otherTeam:
		if (person not in playersInTrick) and (person not in person.game._inactives):
			#player has not gone and is not inactive
			otherTeamStillHasToGo = True
	if not otherTeamStillHasToGo:
		#no one on the other team still has to go
		return cardsThatWouldWin
	#someone on the other team still has to go
	if ledSuit == trump:
		#lead was trump
		if caller in otherTeam:
			#other team called
			right = utils.findCardInCards(cardsThatWouldWin,'J',trump)
			if right!=None:
				#this is the right
				return [right]
			return []
		return cardsThatWouldWin#!!!
	#ledSuit is not trump
	ace = utils.findCardinCards(cardsThatWouldWin,'A',ledSuit)
	if ace!=None:
		return [ace]
	if hasSuit(cardsThatWouldWin,trump,trump):
		return cardsThatWouldWin
	#We don't have shit
	return [utils.best_card(cardsThatWouldWin,trump,ledSuit)]#low chance of working, but give it a try


def findCardinCards(cards, value, suit):
	for card in cards:
		if card[0] == value:
			if card[1] == suit:
				return card
	return None

