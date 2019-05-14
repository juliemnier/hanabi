import hanabi
import hanabi.deck as deck
import hanabi.ai as AI



game=hanabi.Game(2)
ai=AI.MeilleureAI(game)



#ai will clue cG
ai.other_hands[0].cards=[deck.Card(deck.Color.Green, 4), deck.Card(deck.Color.Green, 2), deck.Card(deck.Color.Red, 3), deck.Card(deck.Color.Blue, 5), deck.Card(deck.Color.Green, 3)]
game.turn(ai)


