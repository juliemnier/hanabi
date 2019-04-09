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

        #to clue others

        precious = [ card for card in game.hands[game.other_player].cards
                     if (1+game.discard_pile.cards.count(card))
                         == game.deck.card_count[card.number]
        if precious:
            clue=False
            


        #to discard a card


                     
        #to play a card
        #joue une carte mais sans prendre en compte la couleur des piles déjà faite
        playable = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if game.piles[card.color]+1 == card.number_clue ]

        if card.number_clue==1:
                     
        playable_nocolor_required = [ (i+1, card.number) for (i,card) in
                     enumerate(game.current_hand.cards)
                     if card.number_clue==1 ]
