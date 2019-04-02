import hanabi
import hanabi.ai as ai

#jeu de deux joueurs

game=hanabi.Game(2)
ai=ai.RandomPlaying(game)

ai.play()

#jouer un tour

game.turn()




#jouer toute une partie
