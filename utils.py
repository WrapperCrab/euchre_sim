#import utils.utils as utils

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
		if getCardSuit(card,trump)==suit:
			cardsOfSuit.append(card)
	return cardsOfSuit

def getGreenSuits(trump):
	greenSuits = ['d', 'h', 's', 'c']
	greenSuits.remove(trump)
	greenSuits.remove(same_color(trump))
	return greenSuits

def getSuits():
	return ['d', 'h', 's', 'c']

def hasSuit(cards,trump,suit):
	for card in cards:
		if getCardSuit(card,trump)==suit:
			return True
	return False

def findCardInCards(cards, value, suit):
	for card in cards:
		if card[0]==value and card[1]==suit:
			return card
	return None



