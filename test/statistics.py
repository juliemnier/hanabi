import hanabi
import hanabi.ai as ai


score=[]
for i in range (1000):
    game = hanabi.Game(2)
    AI = ai.RandomPlaying(game)
    game.ai = AI
    game.run()
    score.append(game.score)

print(score)
