
# coding: utf-8

# In[36]:

from bs4 import BeautifulSoup
import urllib
import unicodedata
import re


# In[37]:

#read hyperlinks of plays 
links = []
with open('drama-links.txt', 'r') as f:
    for line in f.readlines():
        if str(line)[0] != '-':
            links.append(str(line).strip())
    

# url = 'http://comediatheque.net/le-joker/'
# url = 'https://fr.wikisource.org/w/index.php?title=Danton_(Romain_Rolland)/Acte_I&printable=yes'
# links.append(url)

webpages = []
for url in links:
    webpages.append(urllib.urlopen(url).read())


# In[38]:

webpage = webpages[0]
# print(webpage)

def parse_webpage(webpage):
    
    soup = BeautifulSoup(webpage, 'html.parser')

    play_tag = soup.find('div', { "class" : "mw-parser-output" })
    all_dTags = play_tag.findAll("div")



    #start of play
    useful_dTags = []
    for s in all_dTags:
        #find div relevant to the play ("personnage" span)
        if s.span:
            class_str = dict(s.span.attrs).get('class', '')
            if u"personnage" in class_str:
                useful_dTags.append(s)

    dialogs = []
    current_dialog = []
    speakers = {}

    # for x in useful_dTags:
    #     print str(x), '\n\n'

    for t in useful_dTags:
        # process every <div> tag

        #speaker processing
        raw_speaker = t.span.get_text()
        raw_speaker = raw_speaker.split('.')[0].split(',')[0]
        raw_speaker = re.sub(r"\(.*\)", "", raw_speaker)
        speaker = raw_speaker.strip()


        if speaker in speakers:
            speaker = speakers[speaker]
        else:
            speakers[speaker] = len(speakers) + 1
            speaker = speakers[speaker]


        ut_s = ''
        dialog_p = t.find_next('p')

        #collapse all contained strings in one
        for s in dialog_p.stripped_strings:    
            long_s = str(s.encode('utf8'))
            #remove parenthesis contents
            long_s = re.sub(r"\(.*\)", "", long_s)

            ut_s += long_s

        result = (speaker, ut_s)
        current_dialog.append(result)

        next_div = t.find_next('div')
        scene_cut = False
        if next_div.span:
            sc_class_str = dict(next_div.span.attrs).get('class', '')
            scene_cut = u"mw-headline" in sc_class_str
        
        if next_div.i or scene_cut:
            #end conversations on non dialog text in a <i> or scene cut
            if len(current_dialog) > 2:
                dialogs.append(current_dialog)
                current_dialog = []
    dialogs.append(current_dialog)
    return dialogs


# In[39]:

plays = []
for page in webpages:
    plays.append(parse_webpage(page))


# In[40]:

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
    print '', nb_conversations, ', ', nb_utt, ', ', avg, ', ', len(speakers)

if total_conversations > 0:
    avg = float(total_utt)/float(total_conversations)
else:
    avg = 'n/a'
print 'Total, , '
print '', total_conversations,', ', total_utt, ', ', avg

result += '</dialog>'

with open('result_drama.xml', 'w') as f:
#     f.write(str(speakers))
    f.write(result)
    
# text is a list of strings (no <p> or any HTML tags in these strings)

