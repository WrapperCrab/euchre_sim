import utils
from player3 import Player3

class PlayerTest(Player3):

    def __init__(self, name):
        self.name = name
        self.game = None
        self.ledSuits = []

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
            cardToPlay = utils.best_card(cards, trumpSuit, None)
            self.ledSuits.append(utils.getCardSuit(cardToPlay,trumpSuit))
            return cardToPlay
        else:
            #find the most likely outride
            likelyOutrides = self.getLikelyOutrides(cards,trumpSuit)
            if len(likelyOutrides)!=0:
                #play the best outride
                cardToPlay = utils.best_card(likelyOutrides, trumpSuit, None)
                self.ledSuits.append(utils.getCardSuit(cardToPlay,trumpSuit))
                return cardToPlay
            # we have no outrides.

            #voidCard = self.getVoidCard(nonTrumpCards, trumpSuit)
            #if (voidCard != None) and (voidCard[0] != 'A'):  # don't discard lone aces
            #    self.ledSuits.append(utils.getCardSuit(voidCard,trumpSuit))
            #    return voidCard
            cardToPlay =utils.best_card(nonTrumpCards, trumpSuit, None)
            self.ledSuits.append(utils.getCardSuit(cardToPlay,trumpSuit))
            return cardToPlay

    def follow(self,trick,playersInTrick):
        trumpSuit = self.game.trump
        cards = self.game.hand_for(self)

        self.ledSuits.append(utils.getCardSuit(trick[0],trumpSuit))


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
            if len(myPlaysThatWin)==0:  # We cannot win
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
            nextSuit = utils.same_color(trump)
            cardsOfNextSuit = utils.getCardsOfSuit(cards, nextSuit, trump)
            if len(cardsOfNextSuit) == 1:
                return cardsOfNextSuit[0]
        return None

    def getLikelyOutrides(self,cards,trump):
        #!!!this function will need to be updated and improved
        # find offsuits that can go all the way through
        outrides = []
        greenSuits = utils.getGreenSuits(trump)
        numCards = len(cards)
        if numCards>=4:
            for suit in greenSuits:
                if suit not in self.ledSuits:
                    #don't lead suits that have already been led
                    cardsOfSuit = utils.getCardsOfSuit(cards, suit, trump)
                    #!!!this does not take into account how far we are into the round
                    if len(cardsOfSuit) > 0:
                        if len(cardsOfSuit) <= .4*float(numCards):
                            # play the ace
                            ace = utils.findCardInCards(cardsOfSuit, 'A', suit)
                            if ace != None:
                                outrides.append(ace)
                        if len(cardsOfSuit) <= .2*float(numCards):
                            # play the king
                            king = utils.findCardInCards(cardsOfSuit, 'K', suit)
                            if king != None:
                                outrides.append(king)
            #			if len(cardsOfSuit) == 1:  # !!!highly doubtful that this is a good idea
            #				# play the queen
            #				queen = findCardInCards(cardsOfSuit, 'Q', suit)
            #				if queen != None:
            #					outrides.append(queen)
            nextSuit = utils.same_color(trump)
            if nextSuit not in self.ledSuits:
                #don't lead a suit that has already been led
                cardsOfNext = utils.getCardsOfSuit(cards, nextSuit, trump)
                if len(cardsOfNext) > 0:
                    if len(cardsOfNext) <= .4*float(numCards):
                        # play the ace
                        ace = utils.findCardInCards(cardsOfNext, 'A', nextSuit)
                        if ace != None:
                            outrides.append(ace)
            #		if len(cardsOfNext) == 1:
            #			# play the king
            #			king = findCardInCards(cardsOfNext, 'K', nextSuit)
            #			if king != None:
            #				outrides.append(king)
            return outrides
        else:
            return []