"""
Artificial Intelligence to play Hanabi.
"""

#note: peut-etre un pb avec la definition du game=self.game au début de chaque fonction, à checker

from hanabi.ai import AI

class MeilleureAI(AI):
    """
    this player plays like we would play
    """

    def play(self):
        """
        return the best action possible
        """
        game = self.game
        playable=always_playable(game.current_hand)
        deduction=self.list_deduction[(self.c_turn)%self.nb_joueurs]
        changed=self.list_changed[(self.c_turn)%self.nb_joueurs]
        #mise à jour de déduction
        if self.c_turn<self.nb_joueurs:
            deduction=self.deduction()
        else:
            if self.actions[(self.c_turn)%self.nb_joueurs][0]==p or self.actions[(self.c_turn)%self.nb_joueurs][0]==d:
                deduction.pop(int(self.actions[(self.c_turn)%self.nb_joueurs][1])-1)
                deduction.append([[1,2,3,4,5],list(hanabi.deck.Color)])

        ##
        liste_rank=list(game.piles.values())
        for list_card in self.list_changed[(self.c_turn)%self.nb_joueurs]:
            #if the clue is on a color and only one card is concerned (cf. strategy)
            if not prev_action[1].isdigit() and len(changed)==1:
                #play the card without question
                return "p%d"%changed[0][0]
            if prev_action[1].isdigit() and ((prev_action[1]-1) in liste_rank):
                #on utilise self.deduction() mais jsp comment
                self.deduction()
                for card in changed:
                    playable.append(card[1])

        #if a card can be played
        if playable:
            #voir si on rajoute les priorités
            return "p%d"%playable[0][0]





    def has_changed(self):
        changed=[]
        prev_hand=prev_hands[0]
        for (i,card) in enumerate(game.current_hand.cards):
            #attention : sous quelle forme est prev_hand ? besoin de .cards ?
            if card.color_clue!=prev_hand[i].color_clue or card.number_clue!=prev_hand[i].number_clue :
                changed.append([i+1,card)] #à tester: peut-être i
        return changed


    def always_playable(self,hand): #à appeler avec game.current_hand et game.next_hand ou l'equivalent

        """
        give a list of cards that are always playable however the current and the other players are playing/deducting

        """
        game = self.game
        always_playable=[]

        #spotting the cards for which we have two clues then filter
        for (i,card) in enumerate(hand.cards):
            if card.color_clue and card.number_clue :
		#checking if playable
                if game.piles[card.color]+1==card.number :
                    alway_playable.append([i+1,card])

	#if all the piles are at the same rank and we own a rank+1
        liste_rank=list(game.piles.values())
        test=liste_rank[0]
        play=True

        for rank in liste_rank:
            if rank!=test:
                play=False
                break
        if play:
            for (i,card) in enumerate(hand.cards):
                if card.number_clue==game.piles[Color.Red]: #Red and any other color have the same rank
                    always_playable.append([i+1,card])

	#if every card with the same rank has already been played or discared

        count=self.global_counter()
        #count is a tab of size 5 which contains the number of remaining card for the ranks 1,2,3,4,5 (in this order)
        interesting=[]
        for (i,value) in enumerate(count):
            if value==1:
                interesting.append(i+1)

        if interesting:
            for rank in interesting:
                for (i,card) in enumerate(hand.cards):
                    if rank-1 in liste_rank and card.number_clue==rank:
                        always_playable.append([i+1,card])

	#see if we find anything else


    def always_discardable(self,hand): #with game.current_hand
        """
        gives a list of cards that are always discardable however the current/other players are playing/deducting
        """

        game = self.game
        always_discardable=[]

        #spotting the cards for which we have two clues then filter
        for (i,card) in enumerate(hand.cards):
            if card.color_clue and card.number_clue :
		#checking if discardable
                if game.piles[card.color]>=card.number :
                    alway_discardable.append([i+1,card])


        #if every rank in the piles is above the rank of one of our card : with one clue only

        liste_rank=list(game.piles.values())
        for (i,card) in enumerate(hand.cards):
            discardable=True
            if card.number_clue: #not necessary but more visible
                for rank in liste_rank:
                    if card.number_clue>rank:
                        discardable=False
                if discardable:
                    alway_discardable.append([i+1,card])

            if game.piles[card.color_clue]==5:
                alway_discardable.append([i+1,card])

        #if the color itself is discardable because all the cards of a rank above the rank of the pile have already been played/discarded

        colorIds={'Red' : 0,'Blue' : 1,'Green' : 2,'White' : 3,'Yellow' : 4}
        counter=self.counter()
        for (i,card) in enumerate(hand.cards):
            if card.color_clue:
                #picking the list corresponding to the card's color
                count= counter[colorIds[str(card.color_clue)]]
                for remaining in count:
                 #   if remaining==0 and ####TO BE CONTINUED
                        alway_discardable.append([i+1,card])



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
        ctr=self.counter()
        #count is a tab of size 5 which contains the number of remaining card for the ranks 1,2,3,4,5 (in this order)
        count=[15,10,10,10,5]
        for i in range(5):
            for color in ctr:
                count[i]-=color[i]


        return count

