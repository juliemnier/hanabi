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
    
