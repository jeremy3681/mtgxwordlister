import json
import re
import requests

wordlist = {}

replacedict= {r'[Äâáà]':'a', r'[Éé]':'e', r'[Öö]':'o', r'[ûůü]':'u', 'ć':'c', 'ř':'r', 'ō':'o',
r'\+(?=\S\/)|(?<=\S\/)\+':'plus', r'-(?=\S\/)|(?<=\S\/)-':'minus', 
r'(?<!\d)1(?!\d)':'one' , r'(?<!\d)2(?!\d)':'two', r'(?<!\d)3(?!\d)':'three', r'(?<!\d)4(?!\d)':'four', r'(?<!\d)5(?!\d)':'five', r'(?<!\d)6(?!\d)':'six', r'(?<!\d)7(?!\d)':'seven', r'(?<!\d)8(?!\d)':'eight', r'(?<!\d)9(?!\d)':'nine', r'(?<!\d)0(?!\d)':'zero',
'\n':' ', '/':'-', r'[˝":;,.!¡∞$\\\?]':'', r'[—−–]':' ', r'[(<].*?[>)]':''}

splitlist={r"[ _]", r"'s |[ _]", r"\-|[ _]"}

def additem(item, score):

    mana =re.findall(r'{.+?}(?!{)',item)
    #for group in mana:

    for key in replacedict:
        item = re.sub(key,replacedict[key],item)


    if 2 < len(item) < 17:
        if item in wordlist:
            wordlist[item]=str(max(score,int(wordlist[item])))
        else:
            wordlist[item]=str(score)

    score = score-5
    for split in splitlist:
        subsplits = re.split(split, item)
        for subsplit in subsplits:
            if 2 < len(subsplit) < 16:
                if subsplit in wordlist:
                    wordlist[subsplit]=str(max(score,int(wordlist[subsplit])))
                else:
                    wordlist[subsplit]=str(score)
    
print ("Generating MTG Crossword List")

url = 'http://mtg.gamepedia.com/api.php'
pagesparam={'action':'query', 'list':'allpages','aplimit':'max','format':'json'}
slangparam={'action':'parse', 'page':'List_of_Magic_slang','prop':'sections', 'format':'json'}

lastContinue = {}
while True:
    req = pagesparam.copy()
    req.update(lastContinue)
    result = requests.get(url, params=req).json()
    for page in result['query']['allpages']:
        additem(page['title'],50)
    if 'continue' not in result:
        break
    lastContinue = result['continue']

slang = requests.get(url,params=slangparam).json()

for section in slang['parse']['sections']:
    additem(section['line'],75)

with open("AllSets-x.json", 'r', encoding="utf-8") as jsonfile:
    sets = json.load(jsonfile)

for set in sets:
    additem(sets[set]["code"],70)
    additem(sets[set]["name"],90)

    for card in sets[set]["cards"]:
        additem(card["name"],100)
        """ if "manaCost" in card:
            additem(card["manaCost"],80) """
        if "text" in card:
            additem(card["text"],60)
        if "flavor" in card:
           additem(card["flavor"],5)

# Print the wordlist dictionary to a file
with open('MTGXWORDLIST.txt', 'w') as listfile:
    for word in wordlist:
        listfile.write(word +';' + wordlist[word] + '\n')

