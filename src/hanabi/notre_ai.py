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
        deduction=self.list_deduction[(self.c_turn)%self.nb_joueurs]
        changed=self.list_changed[(self.c_turn)%self.nb_joueurs]

         #updating deduction with the card played in the player previous turn

        if self.c_turn<self.nb_joueurs:
            deduction=self.deduction()
        else:
            if self.actions[(self.c_turn)%self.nb_joueurs][0]=='p' or self.actions[(self.c_turn)%self.nb_joueurs][0]=='d':
                deduction.pop(int(self.actions[(self.c_turn)%self.nb_joueurs][1])-1)
                deduction.append([[1,2,3,4,5],list(hanabi.deck.Color)])
	    if self.actions[(self.c_turn-1)%self.nb_joueurs][0]=='c':
		for (i,card) in changed:
		    if card.number_clue:
		    	deduction[i-1][0]=card.number_clue
		    if card.color_clue:
			deduction[i-1][1]=card.color_clue

        #deductions : for now, the clue is only to be given to the next player.
	
        prev_action=self.actions[(self.c_turn-1)%self.nb_joueurs]
        liste_rank=list(game.piles.values())
	if prev_action:
            if (prev_action[0]=='c'):
               	#if only one card is concerned (cf. strategy)
               	if len(changed)==1:
                    if changed[0][1].number_clue is False or changed[0][1].color_clue is False:
                    	#play the card without question anyway
                    	self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
                    	self.actions[(self.c_turn)%self.nb_joueurs]= "p%d"%changed[0][0]
                    	self.c_turn+=1
                    	return "p%d"%changed[0][0]
            
            	elif prev_action[1].isdigit():
            	    #more than 2 cards have to be concerned
		    rk=int(prev_action[1])
            	    if list_rank.count((rk-1))!=0 and len(changed)<=list_rank.count(rk-1):
			color=[]
			for i in range(5):
			    if liste_rank[i]==rk-1 : color.append(list(hanabi.deck.Color)[i])
			for (i,card) in changed:
			    #update deduction then playable does the rest
			    deduction[i][1]=color

	self.list_deduction[(self.c_turn)%self.nb_joueurs]=deduction
        playable=self.always_playable()
        discardable=self.always_discardable(game.current_hand)

        #if a card can be played

        if playable:
            #voir si on rajoute les priorités
            self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
            self.actions[(self.c_turn)%self.nb_joueurs]= "p%d"%playable[0][0]
            self.c_turn+=1
            return "p%d"%playable[0][0]


        #beginning the strategy

        if game.blue_coins>0:

            interesting=[]
            #voir ligne 355 deck

            for (i,card) in enumerate(self.other_hands[0].cards):
                if game.piles[card.color]+1 == card.number:
                    interesting.append([i+1,card])


            if interesting:
                for p in interesting:
                    count_rank=0
                    count_color=0
                    for card in self.other_hands[0].cards:
                        if card.number==p[1].number:
                            count_rank+=1
                        if card.color==p[1].color:
                            count_color+=1
                    if p[1].number_clue is False and count_rank==1:
                        self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                        self.actions[(self.c_turn)%self.nb_joueurs]= "c%d"%p[1].number
                        self.c_turn+=1
                        return "c%d"%p[1].number
                    if p[1].color_clue is False and count_color==1:
			clue="c%s"%p[1].color
                        clue=clue[:2]
                        self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                        self.actions[(self.c_turn)%self.nb_joueurs]= clue
                        self.c_turn=self.c_turn+1
                        return clue

                    #when the clue to give is obvious

                    if p[1].number_clue is False and p[1].color_clue :
                        self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                        self.actions[(self.c_turn)%self.nb_joueurs]= "c%d"%p[1].number
                        self.c_turn+=1
                        return "c%d"%p[1].number
                    if p[1].color_clue is False and p[1].number_clue :
                        clue="c%s"%p[1].color
                        clue=clue[:2]
                        self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                        self.actions[(self.c_turn)%self.nb_joueurs]= clue
                        self.c_turn+=1
                        return clue

            #intersections

            if game.blue_coins>1:
                count_rank=[0,0,0,0,0]
                count_color=[['Red',0],['Blue',0],['Green',0],['White',0],['Yellow',0]]

                for card in self.other_hands[0].cards:
                    count_rank[card.number]+=1
                    indice=0
                    for i in count_color:
                        if card.color==count_color[i][0]:
                            indice=i

                    count_color[indice]+=1
                j=0
                maxi=
                best_rank=max(count_rank)
                best_color=max(







    def always_playable(self): 

        """
        give a list of cards that are always playable however the current and the other players are playing/deducting

        """

        game  = self.game
        always_playable=[]

        i=0
        for card in deduction:
            play=True
            for rank in card[0]:
                for color in card[1]:
                    if game.piles[color]+1!=rank:
                        play=False
                        break
                if play == False: break
            if play :
                always_playable.append(game.current_hand.cards[i])
            i+=1
        return always_playable

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


    
    def deduction(self):
        "deduct new clues from the others"
        game = self.game
        counter=self.counter()
        rank=[1,2,3,4,5]
        Color=hanabi.deck.Color
        colors=list(Color)
        deduction=[[rank,colors] for i in game.current_hand.cards]
        clue_rk=[[],[]]
        #deductions from clues
        i=0
        for card in game.current_hand.cards:
            if card.color_clue!=False:
                deduction[i][1]=[card.color]
                clue_rk[1].append(i)
            if card.number_clue!=False:
                deduction[i][0]=[card.number]
                clue_rk[0].append(i)
            i+=1
        #creation of a new counter which takes into account the cards of the others
        colorIds={'Red' : 0,'Blue' : 1,'Green' : 2,'White' : 3,'Yellow' : 4}
        new_counter=counter
        for card in self.other_players_cards:
            tmp=colorIds[str(card.color)]
            new_counter[tmp][card.number-1]=new_counter[tmp][card.number-1]-1
        #deductions from counter
        current_hand=game.current_hand
        for i in clue_rk[0]:
            card=current_hand.cards[i]
            nb=card.number
            for j in list(Color):
                tmp=colorIds[str(j)]
                if new_counter[tmp][nb-1]==0 and j in deduction[i][1]:
                    print(j)
                    print(deduction[i][1])
                    deduction[i][1].remove(j)
        for i in clue_rk[1]:
            card=current_hand.cards[i]
            color=card.color
            tmp=colorIds[str(color)]
            for j in range(1,6):
                if new_counter[tmp][j-1]==0 and j in deduction[i][0]:
                    deduction[i][0].remove(j)
        return deduction
    
