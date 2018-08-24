import json
import re
import requests

wordlist = {}
splitlist={r' ', r'\'s ',r'-',r'_'}
replacedict= {r'[âáà]':'a', 'é':'e', 'ö':'o', r'[ûů]':'u', 'ć':'c', 'ř':'r', 'ō':'o',
'\n':'', r'[˝";?!.,]':'', r'[—_]':' ', r' [(].*[)]':''}



def additem(item, score):
    for key in replacedict:
        item = re.sub(key,replacedict[key],item)

    if not item in wordlist and 2 < len(item) < 15:
        wordlist[item]=str(score)

    for split in splitlist:
        subsplits = re.split(split, item)
        for subsplit in subsplits:
            if not subsplit in wordlist and 2 < len(subsplit) < 15:
                wordlist[subsplit]=str(score-5)
    
print ("Generating MTG Crossword List")

url = 'http://mtg.gamepedia.com/api.php'
request={'action':'query', 'list':'allpages','aplimit':'max','format':'json'}

lastContinue = {}
while True:
    req = request.copy()
    req.update(lastContinue)
    result = requests.get(url, params=req).json()
    for page in result['query']['allpages']:
        additem(page['title'],50)
    if 'continue' not in result:
        break
    lastContinue = result['continue']

with open("AllSets-x.json", 'r', encoding="utf-8") as jsonfile:
    sets = json.load(jsonfile)

for set in sets:
    additem(sets[set]["code"],75)
    additem(sets[set]["name"],100)

    for card in sets[set]["cards"]:
        additem(card["name"],100)
        if "flavor" in card:
            additem(card["flavor"],5)

# Print the wordlist dictionary to a file
with open('MTGXWORDLIST.txt', 'w') as listfile:
    for word in wordlist:
        listfile.write(word +';' + wordlist[word] + '\n')

