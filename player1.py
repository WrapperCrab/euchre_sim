import utils
from player import Player

class Player1(Player):#!!!Does not account for jacks changing suit

	def __init__(self, name):
		Player.__init__(self, name)

	def action(self, trick):
		""" Play a card in trick """
		card_to_play = None
        trumpSuit = self.game.trump

        if not trick:#we are first
            #find highest card overall
            card_to_play = best_card(self.game.hand_for(self), trumpSuit)
            #!!!I don't know if this function works without specifying led suit
        else:#we are not first
            ledSuit = trick[0][1]
            ledSuitCards = []
            for card in self.game.hand_for(self):
                if card[1] == ledSuit:
                    ledSuitCards.append(card) #add this card

            if len(ledSuitCards)==0:
                card_to_play = best_card(self.game.hand_for(self), trumpSuit)
            else:
                card_to_play = best_card(ledSuitCards, trumpSuit, ledSuit)

        return card_to_play


	def call(self, top_card):
		""" Call trump or pass """

        if top_card!=None:
    		numMatch = 0
            for card in self.game.hand_for(self):
                if card[1] == top_card[1]:
                    numMatch++
        	if numMatch >= 2:
                return True
            return False
        else:#there is no top_card
			hCount = 0
			sCount = 0
			cCount = 0
			dCount = 0
			for card in self.game.hand_for(self):
				if card[1]=="h":
					hCount++
				elif card[1]=="s":
					sCount++
				elif card[1]=="c":
					cCount++
				elif card[1]=="d":
					dCount++
				else:
					print("Well shit")
			if hCount>=3:
				return "h"
			elif sCount>=3:
				return "s"
			elif cCount>=3:
				return "c"
			elif dCount>=3:
				return "d"
			elif self.game.position_for(self)!=3:#We are not the dealer
				return False
			else:
				return "h"


	def discard(self):
		""" Choose card to discard after picking up	"""
		for card in self.game.hand_for(self):
			if card[1]!=self.game.trump:
				return card
		return self.game.hand_for(self)[0]#we have only trump

	def end_call(self, caller_position, trump):
		""" Communicate result of calling to player """
		pass

	def end_trick(self):
		""" Communicate result of trick to player """
		pass
