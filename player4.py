import utils
from player3 import Player3

class Player4(Player3):
    def discard(self):
        cards = self.game.hand_for(self)
        trump = self.game.trump
        voidCard = utils.getVoidCard(cards, trump)
        if (voidCard != None) and (voidCard[0]!='A'):#don't discard lone aces
            return voidCard
        #no voiding is possible/necessary
        return utils.worstCard(cards,trump,None)


    def action(self, trick, playersInTrick):
        # Play a card in trick
        if len(trick) == 0:  # we are first
            return self.lead()
        else:  # we are not first
            return self.follow(trick,playersInTrick)

    def lead(self):
        trump = self.game.trump
        cards = self.game.hand_for(self)

        trumpCards = utils.getCardsOfSuit(cards,trump,trump)
        if len(trumpCards)==0:
            #We have no trump. Case 2
            outrides = utils.getLikelyOutrides(cards)#!!!
            if len(outrides)==0:
                return utils.worstCard(cards,trump,None)
            else:
                return utils.best_card(outrides,trump,None)
                #!!!This is flawed since the strongest is not necessarily the most likely
                #Also, we aren't considering playing a suit that our partner does not have
        else:
            #We have trump. Case 1
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
                #find likely outrides
                outrides = utils.getLikelyOutrides(cards)
                if len(outrides)!=0:
                    return utils.best_card(outrides,trump,None)
                else:
                    # We cannot play a card that will go all the way through
                    # try to void in a suit
                    voidCard = utils.getVoidCard(cards, trump)
                    if voidCard != None:
                        return voidCard
                    # voiding is impossible/unnecessary
                    # !!!I am not sure what the best thing to do here would be! I should test for different things
                    return utils.best_card(cards,trump, None)
                    #consider playing low trump if partner called

    def follow(self,trick,playersInTrick):
        trump = self.game.trump
        cards = self.game.hand_for(self)
        team = self.game._teams[self.game.team_num_for(self) - 1]
        ledSuit = utils.getCardSuit(trick[0], trump)

        if utils.hasSuit(cards, trump, ledSuit):
            # We must follow suit
            #case 3
            legalCards = utils.getLegalCards(cards, trump, ledSuit)
            if utils.myTeamIsLikelyToWin():
                return utils.worstCard(legalCards,trump,ledSuit)
            else:#our team is not likely to win
                likelyToWinCards = utils.getCardsThatAreLikelyToWin(trick,playersInTrick,team,trump,legalCards)
                if len(likelyToWinCards)==0:
                    #we can't win
                    return utils.worstCard(legalCards,trump,ledSuit)
                else:
                    #we can win
                    return utils.worstCard(likelyToWinCards,trump,ledSuit)
        else:
            # We don't have to follow suit
            trumpCards = utils.getCardsOfSuit(cards,trump,trump)
            if (len(trumpCards)==0):
                #we have no trump
                #case 5
                return utils.worstCard(cards,trump,ledSuit)
            else:
                #case 4
                if utils.myTeamIsLikelyToWin():
                    voidCard = utils.getVoidCard(cards,trump)
                    if voidCard!=None:
                        return voidCard
                    # no voiding is possible/necessary
                    return utils.worstCard(cards, trump, ledSuit)
                else:#our team is not likely to win
                    likelyToWinCards = utils.getCardsThatAreLikelyToWin(trick, playersInTrick, team, trump, cards)
                    if len(likelyToWinCards) == 0:
                        # we can't win
                        voidCard = utils.getVoidCard(cards, trump)
                        if voidCard != None:
                            return voidCard
                        # no voiding is possible/necessary
                        return utils.worstCard(cards, trump, ledSuit)
                    else:# we can win
                        return utils.worstCard(likelyToWinCards, trump, ledSuit)

"""
            if utils.myTeamIsWinning(trick,playersInTrick,team,trump):  # Our team is winning
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
                if len(myPlaysThatWin) == 0:  # We cannot win
                    voidCard = utils.getVoidCard(cards, trump)
                    if voidCard != None:
                        return voidCard
                    # no voiding is possible/necessary
                    return utils.worstCard(cards, trump, ledSuit)
                else:  # We can win
                    return utils.worstCard(myPlaysThatWin, trump, ledSuit)
                    # !!!worstCard may be better here. May have to split into cases
"""
