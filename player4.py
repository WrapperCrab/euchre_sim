import utils
from player3 import Player3

class Player4(Player3):
    def discard(self):
        cards = self.game.hand_for(self)
        trump = self.game.trump
        voidCard = utils.getVoidCard(cards, trump)
        if voidCard != None:
            return voidCard
        #no voiding is possible/necessary
        return utils.worstCard(cards,trump,None)

"""
    def action(self, trick, playersInTrick):
        #if first, plays highest off suit
        #else, same as Player2

        # Play a card in trick
        trump = self.game.trump
        cards = self.game.hand_for(self)
        team = self.game._teams[self.game.team_num_for(self) - 1]

        if len(trick) == 0:  # we are first
            return self.lead()
        else:  # we are not first
            ledSuit = utils.getCardSuit(trick[0], trump)
            if utils.hasSuit(cards,trump,ledSuit):
                #We must follow suit
                legalCards = utils.getLegalCards(cards, trump, ledSuit)
                if len(legalCards)==1:
                    return legalCards[0]
                #We have more than 1 legal card
                if utils.myTeamIsWinning(trick, trump, playersInTrick, team):  # Our team is winning
                    return utils.worstCard(legalCards,trump,ledSuit)
                    #!!!not always best if partner is sure to lose
                else:  # Our team is losing
                    cardToBeat = utils.best_card(trick, trump, ledSuit)
                    myPlaysThatWin = []
                    for card in legalCards:
                        if utils.best_card([card, cardToBeat], trump, ledSuit) == card:
                            myPlaysThatWin.append(card)
                    if len(myPlaysThatWin)==0:  # We cannot win
                        return utils.worstCard(legalCards, trump, ledSuit)
                    else:  # We can win
                        return utils.worstCard(myPlaysThatWin, trump, ledSuit)
                        #!!!best might be better here. I may have to split cases if ledSuit is trump
            else:
                #We don't have to follow suit
                if utils.myTeamIsWinning(trick, trump, playersInTrick, team):  # Our team is winning
                    voidCard = utils.getVoidCard(cards, trump)
                    if voidCard != None:
                        return voidCard
                    # no voiding is possible/necessary
                    return utils.worstCard(cards, trump, ledSuit)
                else:  # Our team is losing
                    cardToBeat = utils.best_card(trick, trump, ledSuit)
                    myPlaysThatWin = []
                    for card in cards:
                        if utils.best_card([card, cardToBeat], trump, ledSuit) == card:
                            myPlaysThatWin.append(card)
                    if len(myPlaysThatWin)==0:  # We cannot win
                        voidCard = utils.getVoidCard(cards,trump)
                        if voidCard!=None:
                            return voidCard
                        # no voiding is possible/necessary
                        return utils.worstCard(cards, trump, ledSuit)
                    else:  # We can win
                        return utils.worstCard(myPlaysThatWin, trump, ledSuit)
                        #!!!worstCard may be better here. May have to split into cases
"""
"""
    def lead(self):
        trump = self.game.trump
        cards = self.game.hand_for(self)
        # find highest non-trump card
        nonTrumpCards = []
        for card in cards:
            cardSuit = utils.getCardSuit(card, trump)
            if cardSuit != trump:
                nonTrumpCards.append(card)
        if len(nonTrumpCards) == 0:
            # we have only trump
            return utils.best_card(cards, trump, None)
        else:
            # find offsuits that can go all the way through
            greenSuits = utils.getGreenSuits(trump)
            for suit in greenSuits:
                cardsOfSuit = utils.getCardsOfSuit(cards, suit, trump)
                if len(cardsOfSuit) > 0:
                    if len(cardsOfSuit) <= 3:
                        # play the ace
                        ace = utils.findCardInCards(cardsOfSuit, 'A', suit)
                        if ace != None:
                            return ace
                    if len(cardsOfSuit) <= 2:
                        # play the king
                        king = utils.findCardInCards(cardsOfSuit, 'K', suit)
                        if king != None:
                            return king
                    if len(cardsOfSuit) == 1:#!!!highly doubtful that this is a good idea
                        # play the queen
                        queen = utils.findCardInCards(cardsOfSuit, 'Q', suit)
                        if queen != None:
                            return queen
            otherSuit = utils.same_color(trump)
            cardsOfOther = utils.getCardsOfSuit(cards, otherSuit, trump)
            if len(cardsOfOther) > 0:
                if len(cardsOfOther) <= 2:
                    # play the ace
                    ace = utils.findCardInCards(cardsOfOther, 'A', otherSuit)
                    if ace != None:
                        return ace
                if len(cardsOfOther) == 1:
                    # play the king
                    king = utils.findCardInCards(cardsOfOther, 'K', otherSuit)
                    if king != None:
                        return king
        # We cannot play a card that will go all the way through
        # try to void in a suit
        voidCard = utils.getVoidCard(cards, trump)
        if voidCard != None:
            return voidCard
        # voiding is impossible/unnecessary
        # !!!I am not sure what the best thing to do here would be! I should test for different things
        return utils.best_card(cards,trump, None)
        #consider playing low trump if partner called
"""
