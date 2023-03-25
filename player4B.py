import utils
from player3 import Player3

class Player4B(Player3):
    def discard(self):
        cards = self.game.hand_for(self)
        trump = self.game.trump
        voidCard = self.getVoidCard(cards, trump)
        if (voidCard != None) and (voidCard[0]!='A'):#don't discard lone aces
            return voidCard
        #no voiding is possible/necessary
        return utils.worstCard(cards,trump,None)

    def action(self, trick, playersInTrick):
        # Play a card in trick
        if len(trick) == 0:  # we are first
            return self.lead(trick,playersInTrick)
        else:  # we are not first
            return self.follow(trick,playersInTrick)

    def lead(self,trick,playersInTrick):
        trumpSuit = self.game.trump
        cards = self.game.hand_for(self)

        # find highest non-trump card
        nonTrumpCards = []
        for card in cards:
            cardSuit = utils.getCardSuit(card, trumpSuit)
            if cardSuit != trumpSuit:
                nonTrumpCards.append(card)
        if len(nonTrumpCards) == 0:
            # we have only trump
            return utils.best_card(cards, trumpSuit, None)
        else:
            return utils.best_card(nonTrumpCards, trumpSuit, None)

    def follow(self,trick,playersInTrick):
        trumpSuit = self.game.trump
        cards = self.game.hand_for(self)

        ledSuit = utils.getCardSuit(trick[0], trumpSuit)
        legalCards = utils.getLegalCards(cards, trumpSuit, ledSuit)
        team = self.game._teams[self.game.team_num_for(self) - 1]
        if utils.myTeamIsWinning(trick, playersInTrick, team, trumpSuit):  # Our team is winning
            return utils.worstCard(legalCards, trumpSuit, ledSuit)
        else:  # Our team is losing
            cardToBeat = utils.best_card(trick, trumpSuit, ledSuit)
            myPlaysThatWin = []
            for card in legalCards:
                if utils.best_card([card, cardToBeat], trumpSuit, ledSuit) == card:
                    myPlaysThatWin.append(card)
            if not myPlaysThatWin:  # We cannot win
                #try to void in a suit
                voidCard = self.getVoidCard(legalCards, trumpSuit)
                if (voidCard != None) and (voidCard[0] != 'A'):  # don't discard lone aces
                    return voidCard
                # no voiding is possible/necessary
                return utils.worstCard(legalCards, trumpSuit, ledSuit)
            else:  # We can win
                return utils.worstCard(myPlaysThatWin, trumpSuit, ledSuit)

    def getVoidCard(self,cards, trump):
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