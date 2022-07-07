VALUE_MAP = {'9': 1, 'T': 2, 'J': 3, 'Q': 4, 'K': 5, 'A': 6}

def best_card(cards, trump=None, lead=None):
	""" Calculate winning card from list of cards

	Trump and lead suit must be specified, otherwise normal order is assumed.

	I am displeased with the lack of elegance in this function.

	"""
	val_map = {}
	for c in cards:
		val = VALUE_MAP[c[0]]
		if trump == c[1]:#This is trump, maybe right
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


		#Old function that I don't like
		# if lead == c[1]:
		# 	val *= 10
		# if trump == c[1]:
		# 	val *= 100
		# 	if c[0] == 'J':
		# 		val = val*10 + 5
		# if trump == same_color(c[1]) and c[0] == 'J':
		# 	val = val*1000 + 3

		val_map[c] = val

	return sorted(val_map.items(), key=lambda x: x[1], reverse=True)[0][0]

def same_color(suit):
	""" Return other suit of the same same color

	I'm embarrased I had to write this function.

	"""
	if suit == 's':
		return 'c'
	elif suit == 'c':
		return 's'
	elif suit == 'd':
		return 'h'
	elif suit == 'h':
		return 'd'

# Should be unit tests
# print best_card(['Qs', 'As'])
# print best_card(['As', 'Jh'], 'h')
# print best_card(['Jc', 'Js'], 'h', 's')
# print best_card(['Jc', 'Js', 'Jh'], 'h', 's')
# print best_card(['Jc', 'Js', 'Jh', 'Jd'], 'h', 's')
# print best_card(['Jc', 'Js', 'Ah', 'Jd'], 'h', 's')

def getCardSuit(card, trump):#I wrote this
	"""return the true suit of the card"""
	if (card[0]=='J') & (card[1]==same_color(trump)):
		return trump#This is the left
	else:
		return card[1]
