import json
import re

wordlist = {}
replacedict= {u'é':'e', u'â':'a', u'á':'a', u'ö':'o', u'û':'u', u'à':'a', r' [(].*[)]':''}
print ("Opening JSON")
with open('AllCards-x.json', 'r', encoding="utf-8") as jsonfile:
    cards = json.load(jsonfile)


for card in cards.copy():
    asciicard=card
    for key in replacedict:
        asciicard = re.sub(key,replacedict[key],asciicard)
    cards[asciicard] = cards.pop(card)


for card in cards:
        wordlist[card]='100'





#remove small words from the wordlist
for word in wordlist.copy():
    if len(word) <3:
        del wordlist[word]

# Print the wordlist dictionary to a file
with open('MTGXWORDLIST.txt', 'w') as listfile:
    for word in wordlist:
        listfile.write(word +';' + wordlist[word] + '\n')