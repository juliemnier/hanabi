"""
Artificial Intelligence to play Hanabi.
"""

#note: peut-etre un pb avec la definition du game=self.game au début de chaque fonction, à checker

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game


class MeilleureAI(AI):
    """
    this player plays like we would play
    """

    def play(self):
        """
        return the best action possible
        """
        game = self.game

    def always_playable(self):
        """
        give a list of cards that are always playable however the current and the other players are playing/deducting

        """
        game = self.game
        always_playable=[]

        #spotting the cards for which we have two clues then filter
        for card in game.current_hand.cards:
            if card.color_clue and card.number_clue :
		#checking if playable
                if game.piles[card.color]+1==card.number :
                    alway_playable.append(card)

	#if all the piles are at the same rank and we own a rank+1
        liste_rank=list(game.piles.values())
        test=liste_rank[0]
        play=True

        for rank in liste_rank:
            if rank!=test:
                play=False
                break
        if play:
            for card in game.current_hand.cards:
                if card.number_clue==game.piles[Color.Red]: #Red and any other color have the same rank
                    always_playable.append(card)

	#if every card with the same rank has already been played or discared 

        count=global_counter()
        #count is a tab of size 5 which contains the number of remaining card for the ranks 1,2,3,4,5 (in this order)
        interesting=[]
        for (i,value) in enumerate(count):
            if value==1:
                interesting.append(i+1)

        if interesting:
            for rank in interesting:
                for card in game.current_hand.cards:
                    if rank-1 in liste_rank and card.number_clue==rank:
                        always_playable.append(card)

	#see if we find anything else


    def always_discardable(self):
        """
        gives a list of cards that are always discardable however the current/other players are playing/deducting
        """

        game = self.game
        always_discardable=[]
        
        #spotting the cards for which we have two clues then filter
        for card in game.current_hand.cards:
            if card.color_clue and card.number_clue :
		#checking if discardable
                if game.piles[card.color]>=card.number :
                    alway_discardable.append(card)


        #if every rank in the piles is above the rank of one of our card : with one clue only
        
        liste_rank=list(game.piles.values())
        for card in game.current_hand.cards:
            discardable=True
            if card.number_clue: #not necessary but more visible
                for rank in liste_rank:
                    if card.number_clue>rank:
                        discardable=False
                if discardable:
                    alway_discardable.append(card)

            if game.piles[card.color_clue]==5:
                alway_discardable.append(card)

        #if the color itself is discardable because all the cards of a rank above the rank of the pile have already been played/discarded

        colorIds={'Red' : 0,'Blue' : 1,'Green' : 2,'White' : 3,'Yellow' : 4}
        counter=counter()
        for card in game.current_hand.cards:
            if card.color_clue:
                #picking the list corresponding to the card's color
                count= counter[colorIds[str(card.color_clue)]]
                for remaining in count:
                    if remaining==0 and ####TO BE CONTINUED
                    



            #see if we find anything else
    def counter(self):
        """
        look at the table and count the cards played and discared
        """
        counter=[[3,2,2,2,1] for i in range(5)]
        colorIds={'Red' : 0,'Blue' : 1,'Green' : 2,'White' : 3,'Yellow' : 4}
        game = self.game
        for card in game.discard_pile.cards:
            tmp=colorIds[str(card.color)]
            counter[tmp][card.number-1]=counter[tmp][card.number-1]-1
            for (color,i) in list(game.piles.items()):
                if (i!=0) :
                    for j in range(1,i+1):
                        tmp=colorIds[str(color)]
                        counter[tmp][j-1]=counter[tmp][j-1]-1
        return counter


    def global_counter(self):
        """
        look at the table and count the cards played and discared by rank only 
        """
        game=self.game
        ctr=counter()
        #count is a tab of size 5 which contains the number of remaining card for the ranks 1,2,3,4,5 (in this order)
        count=[15,10,10,10,3]
        for i in range(5):
            for color in ctr:
                count[i]-=color[i]


        return count
