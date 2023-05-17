import utils
from player2 import Player2

class Player3(Player2):
    voidAtDiscard = False #add strat for not discarding aces
    switchColor = False
    goAlone = True
    waitForLoner = False

    callPointsForHighTrump = True
    callPointsForVoidOff = False
    callPointsForHighOff = False

    def call(self,top_card):
        cards = self.game.hand_for(self)
        maybeTrump = top_card[1]

        #find number of trump we would have
        maybeCards = cards[:]
        position = self.game.get_player_position(self)
        if position == 3:
            #we are the dealer
            maybeCards.append(top_card)
            maybeCards.remove(self.simulateDiscard(maybeCards,maybeTrump))

        maybeTrumpCards = utils.getCardsOfSuit(maybeCards,maybeTrump,maybeTrump)
        numTrump = len(maybeTrumpCards)

        pointsForCall = 5#!!!These numbers must be tested
        pointsForAlone = 10
        points = 0

        #points for numTrump (base)
        if numTrump>=5:
            points+=10
        elif numTrump>=4:
            points+=8
        elif numTrump>=3:
            points+=5
        elif numTrump>=2:
            points+=3

        #points for high trump
        if self.callPointsForHighTrump:
            maybeHighTrumpCards = []
            right = utils.findCardInCards(maybeCards,'J',maybeTrump)
            if right!=None:
                maybeHighTrumpCards.append(right)
            left = utils.findCardInCards(maybeCards,'J',utils.same_color(maybeTrump))
            if left!=None:
                maybeHighTrumpCards.append(left)
            ace = utils.findCardInCards(maybeCards,'A',maybeTrump)
            if ace!=None:
                maybeHighTrumpCards.append(ace)
            numHighTrump = len(maybeHighTrumpCards)
            if numHighTrump>=3:
                points+=5
            elif numHighTrump>=2:
                points+=3

        #points for voids
        if self.callPointsForVoidOff:
            suits = utils.getSuits()
            suits.remove(maybeTrump)
            numVoidOffs=0
            for suit in suits:
                haveThisSuit = utils.hasSuit(maybeCards,maybeTrump,suit)
                if haveThisSuit==False:
                    numVoidOffs+=1
            if numVoidOffs==3:
                points+=5
            elif numVoidOffs==2:
                points+=3
            elif numVoidOffs==1:
                points+=1

        #points for off aces


        if self.waitForLoner: #only does anything useful if team member sometimes goes alone
            if numTrump<=3 and position == 1 and top_card[0]=='J':
                return False

        if self.goAlone and points>=pointsForAlone:
            return "alone"
        elif points>=pointsForCall:
            return True
        else:
            return False


    def call2(self,top_card):
        cards = self.game.hand_for(self)
        bannedSuit = top_card[1]

        #cycle through each suit
        legalSuits = utils.getSuits()
        legalSuits.remove(bannedSuit)
        for legalSuit in legalSuits:
            pointsForCall = 5
            pointsForAlone = 10
            points = 0

            maybeTrumpCards = utils.getCardsOfSuit(cards,legalSuit,legalSuit)
            numTrump = len(maybeTrumpCards)

            # points for numTrump (base)
            if numTrump >= 5:
                points += 10
            elif numTrump >= 4:
                points += 8
            elif numTrump >= 3:
                points += 5
            elif numTrump >= 2:
                points += 3

            # points for high trump
            if self.callPointsForHighTrump:
                maybeHighTrumpCards = []
                right = utils.findCardInCards(cards, 'J', legalSuit)
                if right != None:
                    maybeHighTrumpCards.append(right)
                left = utils.findCardInCards(cards, 'J', utils.same_color(legalSuit))
                if left != None:
                    maybeHighTrumpCards.append(left)
                ace = utils.findCardInCards(cards, 'A', legalSuit)
                if ace != None:
                    maybeHighTrumpCards.append(ace)
                numHighTrump = len(maybeHighTrumpCards)
                if numHighTrump >= 3:
                    points += 5
                elif numHighTrump >= 2:
                    points += 3

            # points for voids
            if self.callPointsForVoidOff:
                suits = utils.getSuits()
                suits.remove(legalSuit)
                numVoidOffs = 0
                for suit in suits:
                    haveThisSuit = utils.hasSuit(cards, legalSuit, suit)
                    if haveThisSuit == False:
                        numVoidOffs += 1
                if numVoidOffs == 3:
                    points += 5
                elif numVoidOffs == 2:
                    points += 3
                elif numVoidOffs == 1:
                    points += 1

            # points for off aces


            if self.goAlone and points>=pointsForAlone:
                return [legalSuit,"alone"]
            elif points>=pointsForCall:
                return [legalSuit,True]

        #check if we are the dealer
        position = self.game.get_player_position(self)
        if position!=3:
            return [None,False]
        if bannedSuit!="h":
            return ["h",True]
        else:
            return ["d",True]

    def discard(self):
        cards = self.game.hand_for(self)
        trump = self.game.trump

        return self.simulateDiscard(cards,trump)

    def simulateDiscard(self,cards,trump):
        #Try to void
        if self.voidAtDiscard:
            cardsThatVoid = utils.getCardsThatVoid(cards, trump)
            if len(cardsThatVoid) > 0:
                card_to_discard = utils.worstCard(cardsThatVoid, trump, None)
                return card_to_discard

        #base strategy
        return utils.worstCard(cards,trump,None)


