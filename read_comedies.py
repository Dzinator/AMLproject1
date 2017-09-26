
# coding: utf-8

# In[245]:

from bs4 import BeautifulSoup
import urllib
import unicodedata
import re


# In[253]:

#read hyperlinks of plays 
links = []
with open('comedy-links.txt', 'r') as f:
    for line in f.readlines():
        if str(line)[0] != '-':
            links.append(str(line).strip())
    

# url = 'http://comediatheque.net/le-joker/'
# url = 'http://comediatheque.net/le-comptoir/'

webpages = []
for url in links:
    webpages.append(urllib.urlopen(url).read())


# In[260]:

def parse_webpage(webpage):
    
    soup = BeautifulSoup(webpage, 'html.parser')

    all_pTags = soup.find_all('p')

    ind = 0
    for i, s in enumerate(all_pTags):
        #find beginning of play
        found = False
        for strong in s.find_all('strong'):
            if u'TEXTE INTÉGRAL' == s.string or u'TEXTE DE LA PIÈCE À LIRE OU IMPRIMER' == s.string:
                ind = i
                found = True
        if found:
            break

    # useful_pTags contains <p> tags related to the play
    useful_pTags = all_pTags[ind+1:]


    # print str(useful_pTags)
    def parse_dialog(dialog, speakers):
        parts = dialog.split(' – ')

        raw_speaker = re.sub(r"\(.*\)", "", parts[0])
        speaker = raw_speaker.strip()

        utt = parts[1]

        if speaker in speakers:
            speaker = speakers[speaker]
        else:
            speakers[speaker] = len(speakers) + 1
            speaker = speakers[speaker]

        return speaker, utt


    dialogs = []
    current_dialog = []
    speakers = {}

    for t in useful_pTags:
        # process every <p> tag

        ut_s = ''
        foundMarkup = []
        for ut in t.contents:
            if ut.name == 'strong':
                foundMarkup.append('strong')

            elif ut.name == 'a':
                #skip hyperlinks
                foundMarkup.append('a')

            elif ut.name == 'em':
                foundMarkup.append('em')

        #collapse all contained strings in one
        for s in t.stripped_strings:    
            long_s = str(s.encode('utf8'))
            #remove parenthesis contents
            long_s = re.sub(r"\(.*\)", "", long_s)

            ut_s += long_s

        if 'a' in foundMarkup:
            continue
        #skip strong elements as they are not dialogue
        elif 'strong' in foundMarkup:
            dialogs.append(current_dialog)
            current_dialog = []
        elif ' – ' in ut_s:
            if ' – ISBN' in ut_s:
                #end of document
                break
            result = parse_dialog(ut_s, speakers)
            current_dialog.append(result)

        elif 'em' in foundMarkup:
            #end conversations on emphasis non dialog text of length
            if len(current_dialog) > 2:
                dialogs.append(current_dialog)
                current_dialog = []
                
    return dialogs
    # print speakers


# In[261]:

plays = []
for page in webpages:
    plays.append(parse_webpage(page))


# In[266]:

result = '<dialog>\n'
total_conversations = 0
total_utt = 0

for play in plays:
    nb_conversations = 0
    nb_utt = 0

    for dialog in play:
        if len(dialog) == 0:
            continue
        result += '\t<s>\n'
        nb_conversations += 1
        for i, utt in dialog:
            nb_utt += 1

            t_result = '\t\t<utt uid="' + str(i) + '">' + utt + '</utt>\n'
            result += t_result

        result += '\t</s>\n'
        
    total_conversations += nb_conversations
    total_utt += nb_utt
    if nb_conversations > 0:
        avg = float(nb_utt)/float(nb_conversations)
    else:
        avg = 'n/a'
    print '<s>', nb_conversations, '<utt>', nb_utt, 'avg utt/s', avg

if total_conversations > 0:
    avg = float(total_utt)/float(total_conversations)
else:
    avg = 'n/a'
print 'Total'
print '<s>', total_conversations,'<utt>', total_utt, 'avg utt/s', avg

result += '</dialog>'

with open('result.xml', 'w') as f:
#     f.write(str(speakers))
    f.write(result)
    
# text is a list of strings (no <p> or any HTML tags in these strings)

