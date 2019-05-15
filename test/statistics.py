import hanabi
import hanabi.ai as ai


score=[]
red_coins=[]
mean=0
mean_red_coin=0
lose=0
for i in range (1000):
    game = hanabi.Game(2)
    AI = ai.MeilleureAI(game)
    game.ai = AI
    game.run()
    score.append(game.score)
    mean_red_coin+=game.red_coins
    red_coins.append(game.red_coins)
    if game.red_coins == 3: lose+=1
    mean+=game.score

mean=mean/1000
mean_red_coin/=1000
#print(score)
print("Le max est",max(score),".")
print("Le min est",min(score),".")
print("Le score moyen est",mean,".")
print("L'IA à perdu ",lose," fois.")
print("Ils restaient en moyenne",3-mean_red_coin,"jeton(s) rouge(s).")
