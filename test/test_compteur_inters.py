import hanabi
import hanabi.deck as deck
import hanabi.ai as ai

game=hanabi.Game(2)
AI=ai.MeilleureAI(game)

AI.other_hands[0].cards=[deck.Card(deck.Color.Green, 4), deck.Card(deck.Color.Green, 2), deck.Card(deck.Color.Red, 4), deck.Card(deck.Color.Blue, 5), deck.Card(deck.Color.Green, 3)]
AI.other_hands[0].cards[4].color_clue=str(AI.other_hands[0].cards[4].color)[0]
AI.other_hands[0].cards[0].color_clue=str(AI.other_hands[0].cards[4].color)[0]


if game.blue_coins>1:
    count_rank=[[0,0],[0,0],[0,0],[0,0],[0,0]]
    count_color=[['Red',0,0],['Blue',0,0],['Green',0,0],['White',0,0],['Yellow',0,0]]

    for card in AI.other_hands[0].cards:
        count_rank[card.number-1][0]+=1
        if card.number_clue:
            count_rank[card.number-1][1]+=1
        indice=0
        for (i,liste) in enumerate(count_color):
            if str(card.color)==count_color[i][0]:
                indice=i

        count_color[indice][1]+=1
        if card.color_clue:
            count_color[indice][2]+=1
    j_rank=1
    j_color=count_color[0][0]
    maxi_count=count_rank[0][0]-count_rank[0][1]
    maxi_color=count_color[0][1]-count_color[0][2]

    for (i,summ) in enumerate(count_rank):
        if (summ[0]-summ[1])>=maxi_count:
            maxi_count=summ[0]-summ[1]
            j_rank=i+1
    for (i,summ) in enumerate(count_color):
        if (summ[1]-summ[2])>=maxi_color:
            maxi_color=summ[1]-summ[2]
            j_color=summ[0]

print("count color :",maxi_color)
print("count rank :",maxi_count)
print(maxi_count>=maxi_color and maxi_count>=2)
print("c%d"%j_rank)
game.turn(AI)

