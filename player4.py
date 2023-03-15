import utils
from player3 import Player3

class Player4(Player3):
    def discard(self):
        cards = self.game.hand_for(self)
        trump = self.game.trump

        greenSuits = ['d','h','s','c']
        greenSuits.remove(trump)
        greenSuits.remove(utils.same_color(trump))

    def action(self, trick, playersInTrick):
        #if first, plays highest off suit
        #else, same as Player2

        # Play a card in trick
        card_to_play = None
        trumpSuit = self.game.trump
        myHand = self.game.hand_for(self)

        if len(trick) == 0:  # we are first
            # find highest non-trump card
            nonTrumpCards = []
            for card in myHand:
                cardSuit = utils.getCardSuit(card,trumpSuit)
                if cardSuit!=trumpSuit:
                    nonTrumpCards.append(card)
            if len(nonTrumpCards)==0:
                #we have only trump
                return utils.best_card(myHand,trumpSuit,None)
            else:
                return utils.best_card(nonTrumpCards,trumpSuit,None)
        else:  # we are not first
            ledSuit = utils.getCardSuit(trick[0], trumpSuit)
            myPlays = utils.getLegalCards(myHand, trumpSuit, ledSuit)
            team = self.game._teams[self.game.team_num_for(self) - 1]
            if utils.myTeamIsWinning(trick, trumpSuit, playersInTrick, team):  # Our team is winning
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


