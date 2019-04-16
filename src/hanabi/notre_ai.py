"""
Artificial Intelligence to play Hanabi.
"""

class MeilleureAI(AI):
    """
    this player plays like we would play
    """

    def play(self):
        """
        return the best action possible
        """
        game = self.game


	"""
		determine the list of cards that are playable without using deduction
	"""
	
	always_playable=[]
	#on ajoute les cartes dont on connait les deux indices, penser à filtrer après
	for card in game.current_hand.cards:
		if card.color_clue and card.number_clue :
		#on verifie qu'elles sont jouables
			if game.piles[card.color]+= card.number : 			
				alway_playable.append(card)
	#si on a toutes les couleurs des piles au même numéro et qu'on possède le numéro
	liste_rank=list(game.piles.values())
	test=liste_test[0]
	play=True
	for rank in liste_rank:
		if rank!=test:
			play=False
			break
	if play:
		for card in game.current_hand.cards:
			if card.number_clue==game.piles[Color.Red]: #toutes les valeurs sont les mêmes, on prend Red au hasard
				always_playable.append(card)
	
	#toutes les autres cartes du même numéro ont été jouées

	#un petit compteur "global":

	ctr=counter()
	interesting=[]
	count=[15,10,10,10,3]
	int
	for i in range(5):
		for color in ctr:
			count[i]-=color[i]
	
	for i in count:
		if i==1:
			interesting.append(i)

	if interesting:
		for i in interesting:
			for card in game.current_hand.cards:
				if i-1 in liste_rank and card.number_clue==1:
					always_playable.append(card)
	
	#voir si on trouve d'autres cas
		
	"""
		determine is a card is discardable or not
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




###SIMPLE COPIE POUR L'INSTANT
        #to clue others

        precious = [ card for card in game.hands[game.other_player].cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
        if precious:
            clue=False
            

                     
        #to play a card
        #joue une carte mais sans prendre en compte la couleur des piles déjà faite
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number_clue ]

        if card.number_clue==1:
                     
        playable_nocolor_required = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if card.number_clue==1 ]
