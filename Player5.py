import utils
from player4B import Player4B

class Player5(Player4B):
    def call(self, topCard):
        callStrength = 2
        lonerStrength = 2.5
        handStrength = 0
        for card in self.game.hand_for(self):
            handStrength += self.getStrengthOfCard(card,topCard[1])
        position = self.game.get_player_position(self)
        if position ==3:
            #also find the strength of the topCard
            handStrength += self.getStrengthOfCard(topCard,topCard[1])
        if handStrength>=lonerStrength:
            return "alone"
        elif handStrength>=callStrength:
            return True
        else:
            return False

    def call2(self, topCard):
        bannedSuit = topCard[1]
        suits = utils.getSuits()
        suits.remove(bannedSuit)
        for suit in suits:
            callStrength = 2
            lonerStrength = 2.5
            handStrength = 0
            for card in self.game.hand_for(self):
                handStrength += self.getStrengthOfCard(card, suit)
            if handStrength >= lonerStrength:
                return [suit,"alone"]
            elif handStrength >= callStrength:
                return [suit,True]
        position = self.game.get_player_position(self)
        if position ==3:
            #just randomly call legal suit
            return [suits[0],True]
        return [None,False]


    def getStrengthOfCard(self,card, trump):
        #a general heuristic for the strength of a card when calling trump
        if utils.getCardSuit(card,trump)==trump:
            #this is trump
            if card[0]=='J':
                if card[1]==trump:
                    #this is the right
                    return 1.0
                else:
                    #this is the left
                    return .8
            elif card[0]=='A':
                return .6
            elif card[0]=='K':
                return .3
            elif card[0]=='Q':
                return .2
            elif card[0]=='T':
                return .2
            elif card[0]=='9':
                return .2
        else:
            #this is not trump
            if card[0]=='A':
                return .5
            elif card[0]=='K':
                return .2
        return 0


