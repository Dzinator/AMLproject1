
# coding: utf-8

# In[ ]:

from bs4 import BeautifulSoup
import urllib
import unicodedata
import re


# In[38]:

#read hyperlinks of plays 
links = []
# with open('comedy-links.txt', 'r') as f:
#     for line in f.readlines():
#         if str(line)[0] != '-':
#             links.append(str(line).strip())
    

# url = 'http://comediatheque.net/le-joker/'
url = 'https://fr.wikisource.org/w/index.php?title=Danton_(Romain_Rolland)/Acte_I&printable=yes'
links.append(url)

webpages = []
for url in links:
    webpages.append(urllib.urlopen(url).read())


# In[ ]:

webpage = webpages[0]
# print(webpage)
soup = BeautifulSoup(webpage, 'html.parser')

all_dTags = soup.findAll("div")

#start
useful_dTags = []
for i, s in enumerate(all_dTags):
    #find div relevant to the play ("personnage" span)
    for span in s.find_all('span', { "class" : "personnage" }):
        useful_dTags.append(s)


dialogs = []
current_dialog = []
speakers = {}

print len(useful_dTags)

for t in useful_dTags:
    # process every <div> tag
    
    #speaker processing
    for span in t.find_all('span', { "class" : "personnage" }):
        raw_speaker = str(span.string)
        break
    print raw_speaker
    raw_speaker = re.sub(r"\(.*\)", "", raw_speaker)
    speaker = raw_speaker.strip()
   

    if speaker in speakers:
        speaker = speakers[speaker]
    else:
        speakers[speaker] = len(speakers) + 1
        speaker = speakers[speaker]

    
    ut_s = ''
    foundMarkup = []
#     for ut in t.contents:
#         if ut.name == 'strong':
#             foundMarkup.append('strong')

#         elif ut.name == 'a':
#             #skip hyperlinks
#             foundMarkup.append('a')

#         elif ut.name == 'em':
#             foundMarkup.append('em')

    #collapse all contained strings in one
    nexts = t.next_siblings
    for n in nexts:
        if n.name == 'p':
            dialog_p = n
            break
    print str(dialog_p)
    if dialog_p.string:
        long_s = str(dialog_p.string.encode('utf8'))
        #remove parenthesis contents
        long_s = re.sub(r"\(.*\)", "", long_s)

        ut_s = long_s
    else:
        for s in dialog_p.stripped_strings:    
            long_s = str(s.encode('utf8'))
            #remove parenthesis contents
            long_s = re.sub(r"\(.*\)", "", long_s)

            ut_s += long_s
        
    result = (speaker, ut_s)
    print result
    current_dialog.append(result)

#     if 'a' in foundMarkup:
#         continue
#     #skip strong elements as they are not dialogue
#     elif 'strong' in foundMarkup:
#         dialogs.append(current_dialog)
#         current_dialog = []
#     elif ' – ' in ut_s:
#         if ' – ISBN' in ut_s:
#             #end of document
#             break
#         result = parse_dialog(ut_s, speakers)
#         current_dialog.append(result)

#     elif 'em' in foundMarkup:
#         #end conversations on emphasis non dialog text of length
#         if len(current_dialog) > 2:
#             dialogs.append(current_dialog)
#             current_dialog = []

# return dialogs
# print speake


# In[ ]:

def parse_webpage(webpage):
    
    soup = BeautifulSoup(webpage, 'html.parser')

    all_dTags = soup.find_all('div')

    #start
    ind = 0
    for i, s in enumerate(all_dTags):
        #find beginning of play
        found = False
        for span in s.find_all('span'):
            if span['class'] == 'personnage':
                ind = i
                found = True
        if found:
            break

    # useful_dTags contains <div> tags related to the play
    useful_dTags = all_dTags[ind:]


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

