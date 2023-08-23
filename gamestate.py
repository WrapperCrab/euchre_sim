import utils

#for now, gamestate only contains data for a single hand
class Gamestate:
    players = ["Soud","Wes","Nora","Ean"]
    score = {"NS":0,"WE":0}
    hands = {"Soud": [],"Wes": [], "Nora": [], "Ean": []}
    playedCards = []
    trick = []
    nextPlayer = "Soud"
    trump = None

    def __init__(self,teamNSScore,teamWEScore,sHand,wHand,nHand,eHand,trick,playedCards,nextPlayer,trump):
        self.score["NS"] = teamNSScore
        self.score["WE"] = teamWEScore
        self.hands["Soud"] = sHand
        self.hands["Wes"] = wHand
        self.hands["Nora"] = nHand
        self.hands["Ean"] = eHand

        self.trick = trick
        self.playedCards = playedCards
        self.nextPlayer = nextPlayer
        self.trump = trump

    def getLegalMoves(self):
        hand = self.hands[self.nextPlayer]
        if len(self.trick)==0:
            return hand
        else:
            #must match led suit
            ledSuit = utils.getCardSuit(self.trick[0],self.trump)
            legalMoves = []
            for card in hand:
                cardSuit = utils.getCardSuit(card,self.trump)
                if cardSuit==ledSuit:
                    legalMoves.append(card)
            if len(legalMoves)>0:
                return legalMoves
            return hand

    def doMove(self,move):#move is a card
        hand = self.hands[self.nextPlayer]
        if move not in hand:
            raise Exception("Move not in hand")
            return
        legalMoves = self.getLegalMoves()
        if move not in legalMoves:
            raise Exception("Move not legal")
            return

        self.hands[self.nextPlayer].remove(move)
        self.trick.append(move)
        if len(self.trick)<4:
            index = self.players.index(self.nextPlayer)
            newIndex = (index+1)%4
            self.nextPlayer = self.players[newIndex]
        else:
            #determine winner, update nextPlayer, update score, move trick to cardsPlayed
            ledSuit = utils.getCardSuit(self.trick[0],self.trump)
            winningMove = utils.best_card(self.trick,self.trump,ledSuit)
            winningMoveIndex = self.trick.index(winningMove)
            nextPlayerIndex = self.players.index(self.nextPlayer)
            winningPlayerIndex = (nextPlayerIndex+winningMoveIndex-3)%4
            winningPlayer = self.players[winningPlayerIndex]
            self.nextPlayer = winningPlayer
            winningTeam = self.getTeamToMove()
            self.score[winningTeam]+=1

            for card in self.trick:
                self.cardsPlayed.append(card)
            self.trick = []

    def getWinner(self):
        if self.score["NS"]+self.score["WE"]==5:
            if self.score["NS"]>self.score["WE"]:
                return "NS"
            return "WE"
        return None

    def getTeamToMove(self):#This function assumes no mistaken input
        if self.nextPlayer=="Soud" or self.nextPlayer=="Nora":
            return "NS"
        else:
            return "WE"

    def getOtherTeam(self,team):#This function assumes no mistaken input
        if team=="NS":
            return "WE"
        else:
            return "NS"