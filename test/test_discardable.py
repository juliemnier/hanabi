import hanabi
import hanabi.ai as ai
import hanabi.deck as deck

game=hanabi.Game(2)
AI=ai.MeilleureAI(game)


def test_discardable():
    game.piles[deck.Color.Red]=5
    A=deck.Card(deck.Color.Red,1)
    deduction=[[[1],[deck.Color.Red]]]
    if AI.always_discardable(deduction)[0][1]==game.current_hand.pop(1):
        return True
