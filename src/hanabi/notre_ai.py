"""
Artificial Intelligence to play Hanabi.
"""

#note: peut-etre un pb avec la definition du game=self.game au début de chaque fonction, à checker
#ne pas oublier d'incrémenter le nb de tours
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
        #attention : à changer si on change always_playable(self)
        playable=self.always_playable(game.current_hand)
        discardable=self.always_discardable(game.current_hand)
        #mise à jour de actions, liste tournante

        player=self.c_turn

        #deductions
        prev_action=actions[(player-1)%self.nb_joueurs]
        liste_rank=list(game.piles.values())
        changed=self.list_changed[(self.c_turn)%self.nb_joueurs]
        
        if (prev_action[0]==c):
            #if the clue is on a color and only one card is concerned (cf. strategy)
            if not prev_action[1].isdigit() and len(changed)==1:
                #play the card without question
                self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
                return "p%d"%changed[0][0]
            if prev_action[1].isdigit():
                if ((int(prev_action[1])-1) in liste_rank):
                    #on utilise self.deduction() mais jsp comment
                    self.deduction()
                    for card in changed:
                        playable.append(card)
                trouve=False
                for rank in liste_rank:
                    if rank>=prev_action[1]:
                        trouve=True
                        break
                if not trouve:
                    for card in changed:
                        discardable.append(card)



        #if a card can be played

        if playable:
            #voir si on rajoute les priorités
            self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
            #remplacer dans actions
            return "p%d"%playable[0][0]


        #beginning the strategy

        if game.blue_coins>0:

            interesting=[]

            player=1
            for (i,card) in enumerate(self.other_hands.cards):
                if i%5==0:
                    player+=1
                if game.piles[card.color]+1 == card.number ]:
                    interesting.append([player, i+1, card.number])


            if interesting:
                trouve=False
            
                for (j,move) in enumerate(interesting):
                    concerned_player=interesting[j][0]
                    





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
                if card in self.other_players_cards :
                    #voir si on garde dans discardable
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
