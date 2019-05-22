import hanabi
import hanabi.ai as AI

game=hanabi.Game(2)
ai=AI.MeilleureAI(game)
game.ai=ai
game.run()
