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
