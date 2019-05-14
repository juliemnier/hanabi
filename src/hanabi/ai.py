"""
Artificial Intelligence to play Hanabi.
"""
import random as rd
import hanabi

import itertools

class AI:
    """
    AI base class: some basic functions, game analysis.
    """
    def __init__(self, game):
        self.game = game
        self.c_turn = 0 #Counter of turn
        self.nb_joueurs = len(game.players) #Number of players
        self.list_deduction=[[] for i in range(self.nb_joueurs)] #A list of lists deductions (cf self.deduction) 
        self.actions=[[] for i in range(self.nb_joueurs)] #A list with the memory of the previous actions for each player.[action]
        self.list_changed=[[] for i in range(self.nb_joueurs)] #A list with the memory of the card which have changed for each player during the turn of another player.[[[index of the card,card changed]]]
    
        
    @property
    def other_hands(self):
        "The list of other players' hands."
        return self.game.hands[1:]

    @property
    def other_players_cards(self):
        "All of other players's cards, concatenated in a single list."
        #return sum([x.cards for x in self.other_hands], [])
        return list(itertools.chain.from_iterable([hand.cards for hand in self.other_hands]))

        
class Cheater(AI):
    """
    This player can see his own cards!

    Algorithm:
      * if 1-or-more card is playable: play the lowest one, then newest one
      * if blue_coin<8 and an unnecessary card present: discard it.
      * if blue_coin>0: give a clue on precious card (so a human can play with a Cheater)
      * if blue_coin<8: discard the largest one, except if it's the last of its kind or in chop position in his opponent.
    """
    def counter(self):
        "look at the table and count the cards"
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
    
    def play(self):
        "Return the best cheater action."
        game = self.game
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number ]

        if playable:
            # sort by ascending number, then newest
            playable.sort(key=lambda p: (p[1], -p[0]))
            print ('Cheater would play:', "p%d"%playable[0][0], end=' ')
            if (len(playable)>1):
                print('but could also pick:', playable[1:])
            else: print()

            return "p%d"%playable[0][0]


        discardable = [ i+1 for (i,card) in
                        enumerate(game.current_hand.cards)
                        if ( (card.number <= game.piles[card.color])
                             or (game.current_hand.cards.count(card)>1)
                        ) ]
        # discard already played cards, doubles in my hand
        # fixme: discard doubles, if I see it in partner's hand
        # fixme: il me manque les cartes sup d'une pile morte

        if discardable and (game.blue_coins<8):
            print ('Cheater would discard:', "d%d"%discardable[0], discardable)
            return "d%d"%discardable[0]

        ## 2nd type of discard: I have a card, and my partner too
        
        discardable2 = [ i+1 for (i,card) in enumerate(game.current_hand.cards)
                         if card in self.other_players_cards
                       ]
        if discardable2 and (game.blue_coins<8):
            print ('Cheater would discard2:', "d%d"%discardable2[0], discardable2)
            return "d%d"%discardable2[0]
        

        ## Look at precious cards in other hand, to clue them
        precious = [ card for card in
                     self.other_players_cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
                   ]
        if precious:
            clue = False
            # this loop is such that we prefer to clue an card close to chop
            # would be nice to clue an unclued first, instead of a already clued
            for p in precious:
                #print (p, p.number_clue, p.color_clue)
                if p.number_clue is False:
                    clue = "c%d"%p.number
                    break
                if p.color_clue is False:
                    clue = "c%s"%p.color
                    clue = clue[:2]   # quick fix, with 3+ players, can't clue cRed anymore, only cR
                    break
                # this one was tricky:
                # don't want to give twice the same clue
            if clue:
                print ('Cheater would clue a precious:',
                       clue, precious)
                if game.blue_coins>0:
                    return clue
                print ("... but there's no blue coin left!")


        # if reach here, can't play, can't discard safely, no card to clue-save
        # Let's give a random clue, to see if partner can unblock me
        if game.blue_coins >0:
            print ('Cheater would clue randomly: cW')
            return 'cw'

        # If reach here, can't play, can't discard safely
        # No blue-coin left.
        # Must discard a card. Let's choose a non-precious one (preferably a 4)
        mynotprecious = [ (card.number,i+1) for (i,card) in
                          enumerate(game.current_hand.cards)
                          if not (
                                  (1+game.discard_pile.cards.count(card))
                                  == game.deck.card_count[card.number])
                     ]
        mynotprecious.sort(key=lambda p: (-p[0], p[1]))
        if mynotprecious:
            act = 'd%d'%mynotprecious[0][1]
            print('Cheater is trapped and must discard:', act, mynotprecious)
            return act

        # Oh boy, not even a safe discard, this is gonna hurt!
        # it's a loss. Discard the biggest
        myprecious = [ (card.number,i+1) for (i,card) in enumerate(game.current_hand.cards) ]
        myprecious.sort(key=lambda p: (-p[0], p[1]))
        act = 'd%d'%myprecious[0][1]
        print('Cheater is doomed and must discard:', act, myprecious)
        return act


class RandomPlaying(AI):
    """
    this player does things randomly (without cheating!) modification2

    """
    def play(self):
        """
        return a random action
        """
        game=self.game

        #choosing a random action

        acts=['d','p','c']
        do=rd.choice(acts)

        #choosing a random card from your hand

        i=rd.randint(0,4)
        #mycard=game.current_hand.cards[i]

        if (do=='p'):
            return "p%d"%i
        if (do=='d'):
            return "d%d"%i

        if (do=='c'):
            if game.blue_coins>0:
                while True:
                    j=rd.randint(0,4)
                    cardchosen=game.hands[game.other_player].cards[j]
                    if cardchosen.number_clue == False: 
                        return "c%d"%cardchosen.number
                    if cardchosen.color_clue == False:
                        return "c%s"%cardchosen.color
            else:
                return "d%d"%i

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
        playable=self.always_playable(deduction)
        #discardable=self.always_discardable(game.current_hand)

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
                        self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
                        self.actions[(self.c_turn)%self.nb_joueurs]= "c%d"%p[1].number
                        self.c_turn+=1
                        return "c%d"%p[1].number
                    if p[1].color_clue is False and count_color==1:
                        clue="c%s"%p[1].color
                        clue=clue[:2]
                        self.list_changed[(self.c_turn)%self.nb_joueurs]=[]        
                        self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                        self.actions[(self.c_turn)%self.nb_joueurs]= clue
                        self.c_turn=self.c_turn+1
                        return clue

                    #when the clue to give is obvious

                    if p[1].number_clue is False and p[1].color_clue :
                        self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
                        self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                        self.actions[(self.c_turn)%self.nb_joueurs]= "c%d"%p[1].number
                        self.c_turn+=1
                        return "c%d"%p[1].number
                    if p[1].color_clue is False and p[1].number_clue :
                        clue="c%s"%p[1].color
                        clue=clue[:2]
                        self.list_changed[(self.c_turn)%self.nb_joueurs]=[]        
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
                        #peut etre str(card.color)
                        if str(card.color)==count_color[i][0]:
                            indice=i

                    count_color[indice][1]+=1
                j_rank=0
                j_color=0
                maxi_count=count_rank[0]
                maxi_color=count_color[0][0]

                for (i,sum) in enumerate(count_rank):
                    if sum>=maxi_count:
                        maxi_count=sum
                        j_rank=i
                for (i,sum) in enumerate(count_color):
                    if sum[1]>=maxi_color:
                        maxi_color=sum[1]
                        j_color=sum[0]
                if maxi_count>=maxi_color and maxi_count>=2:
                    for p in self.other_hands[0].cards:
                        if p.number==j_rank:
                            self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                    self.actions[(self.c_turn)%self.nb_joueurs]= "c%d"%j_rank
                    self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
                    self.c_turn+=1
                    return "c%d"%j_rank
                if maxi_count<maxi_color and maxi_color>=2:
                    for p in self.other_hands[0].cards:
                        if p.color==j_color:
                            self.list_changed[(self.c_turn+1)%self.nb_joueurs].append(p)
                    clue="c%s"%j_color
                    clue=clue[:2]
                    self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
                    self.actions[(self.c_turn)%self.nb_joueurs]= clue
                    self.c_turn+=1
                    return clue
        #discard a card
        #if discardable:
         #   self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
          #  self.actions[(self.c_turn)%self.nb_joueurs]= "d%d"%discardable[0][0]
           # self.c_turn+=1
            #return "d%d"%discardable[0][0]

        #last resort

        for (i,card) in enumerate(game.current_hand.cards):
            if not card.number_clue or not card.color_clue:
                self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
                self.actions[(self.c_turn)%self.nb_joueurs]= "d%d"%(i+1)
                self.c_turn+=1
                return "d%d"%(i+1)


        self.list_changed[(self.c_turn)%self.nb_joueurs]=[]
        self.actions[(self.c_turn)%self.nb_joueurs]= "d%d"%discardable[0][0]
        self.c_turn+=1
        return "d%d"%5







    def always_playable(self,deduction): 

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


    def always_discardable(self,deduction): #with game.current_hand
        """
        gives a list of cards that are always discardable however the current/other players are playing/deducting
        """

        game  = self.game
        always_dicardable=[]

        #search for the dead colors
        dead_color={}
        colorIds={'Red' : 0,'Blue' : 1,'Green' : 2,'White' : 3,'Yellow' : 4}
        counter=self.counter()
        for color in list(hanabi.deck.Color):
            tmp=colorIds[str(color)]
            L=counter[tmp]
            if 0 in L:
                dead_color[color]=L.index(0)

                #search for the cards which are discardable
        i=0
        for card in deduction:
            discard=True
            for rank in card[0]:
                for color in card[1]:
                    if game.piles[color]<rank:
                        discard=False
                        if (color in list(dead_color.keys()) and rank>dead_color.get(color)):
                            discard=True
                    if discard == False: break
                if discard == False: break
            if discard :
                always_discardable.append([i+1,game.current_hand.cards[i]])
            i+=1
        return always_discardable

       
     

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
    





