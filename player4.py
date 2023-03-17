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
            outrides = self.getLikelyOutrides(cards,trump)
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
                outrides = self.getLikelyOutrides(cards,trump)
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
                    return utils.worstCard(cards,trump, None)
                    #consider playing low trump if partner called

    def follow(self,trick,playersInTrick):
        trump = self.game.trump
        cards = self.game.hand_for(self)
        team = self.game._teams[self.game.team_num_for(self) - 1]
        otherTeam = self.game._teams[self.game.team_num_for(self)%2]
        ledSuit = utils.getCardSuit(trick[0], trump)
        caller = self.game._caller

        if utils.hasSuit(cards, trump, ledSuit):
            # We must follow suit
            #case 3
            legalCards = utils.getLegalCards(cards, trump, ledSuit)
            caller = self.game._caller
            if self.myTeamIsLikelyToWin(trick,playersInTrick,team,trump,self,caller):
                return utils.worstCard(legalCards,trump,ledSuit)
            else:#our team is not likely to win
                likelyToWinCards = self.getCardsThatAreLikelyToWin(trick,playersInTrick,team,otherTeam,caller,trump,legalCards)
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
                if self.myTeamIsLikelyToWin(trick,playersInTrick,team,trump,self,caller):
                    voidCard = utils.getVoidCard(cards,trump)
                    if voidCard!=None:
                        return voidCard
                    # no voiding is possible/necessary
                    return utils.worstCard(cards, trump, ledSuit)
                else:#our team is not likely to win
                    likelyToWinCards = self.getCardsThatAreLikelyToWin(trick, playersInTrick, team, otherTeam, caller, trump, cards)
                    if len(likelyToWinCards) == 0:
                        # we can't win
                        voidCard = utils.getVoidCard(cards, trump)
                        if voidCard != None:
                            return voidCard
                        # no voiding is possible/necessary
                        return utils.worstCard(cards, trump, ledSuit)
                    else:# we can win
                        return utils.worstCard(likelyToWinCards, trump, ledSuit)

    def getCardsThatAreLikelyToWin(self, trick,playersInTrick,team,otherTeam,caller,trump,cards):
        ledSuit = utils.getCardSuit(trick[0], trump)
        cardsThatWouldWin = []
        bestCard = utils.best_card(trick)
        for card in cards:
            if card == utils.best_card([card,bestCard], trump, ledSuit):
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
        ace = utils.findCardInCards(cardsThatWouldWin, 'A', ledSuit)
        if ace!=None:
            return [ace]
        if utils.hasSuit(cardsThatWouldWin,trump,trump):
            return cardsThatWouldWin
        #We don't have shit
        return [utils.best_card(cardsThatWouldWin,trump,ledSuit)]#low chance of working, but give it a try

    def myTeamIsLikelyToWin(self,trick,playersInTrick,team,trump,player,caller):
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


    def getLikelyOutrides(self,cards,trump):
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
    #				queen = findCardInCards(cardsOfSuit, 'Q', suit)
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
    #			king = findCardInCards(cardsOfOther, 'K', otherSuit)
    #			if king != None:
    #				outrides.append(king)
        return outrides



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


