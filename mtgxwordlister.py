import json
print ("Opening JSON")
with open('AllCards-x.json', 'r') as jsonfile:
    cards = json.load(jsonfile)

file = open('MTGXWORDLIST.txt', 'w')
for card in cards:
    if card.isalpha():
        file.write(card+';'+'100\n')

file.close()

""" 
for card in cards:
    if not all(c.isalpha() or c.isspace() for c in card):
        print(card)
 """