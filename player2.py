import utils
from player1B import Player1B

class Player2(Player1):
	def action(self, trick, playersInTrick):
		#Play a card in trick
		card_to_play = None
		trumpSuit = self.game.trump
		myHand = self.game.hand_for(self)

		if len(trick)==0:#we are first
			#find highest card overall
			card_to_play = utils.best_card(myHand, trumpSuit, None)
		else:#we are not first
			ledSuit = utils.getCardSuit(trick[0],trumpSuit)
			myPlays = utils.getLegalCards(myHand, trumpSuit, ledSuit)
			team = self.game._teams[self.game.team_num_for(self)-1]
			if utils.myTeamIsWinning(trick, trumpSuit, playersInTrick, team):#Our team is winning
				card_to_play = utils.worstCard(myPlays, trumpSuit, ledSuit)
			else:#Our team is losing
				cardToBeat = utils.best_card(trick, trumpSuit, ledSuit)
				myPlaysThatWin = []
				for card in myPlays:
					if utils.best_card([card, cardToBeat], trumpSuit, ledSuit)==card:
						myPlaysThatWin.append(card)
				if not myPlaysThatWin:#We cannot win
					card_to_play = utils.worstCard(myPlays, trumpSuit, ledSuit)
				else:#We can win
					card_to_play = utils.worstCard(myPlaysThatWin, trumpSuit, ledSuit)
		return card_to_play
