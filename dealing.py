import random
dic={"2", "3","4","5","6","7","8","9","10","J","Q","K","A"}
dic3=["Heart","Spade","Diamond","Club"]
card = []
for a in dic3:
    for b in dic:
        card.append([a,b])

print(card)
print(len(card))
random.shuffle(card)
print(card)





