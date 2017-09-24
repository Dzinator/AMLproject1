
# coding: utf-8

# In[56]:

from bs4 import BeautifulSoup
import urllib2
import unicodedata


# In[70]:

url = 'http://comediatheque.net/le-joker/'
# url = 'http://comediatheque.net/librairie-theatrale-en-ligne-achat-livre/'

webpage = urllib2.urlopen(url).read().decode('utf8')

webpage = unicodedata.normalize("NFKD", webpage).replace('&nbsp;', '')

#webpage = webpage.decode('unicode_escape').replace('\xa0',' ').encode('ascii','ignore')


#print webpage

soup = BeautifulSoup(webpage, 'html')
print soup.prettify()


# In[62]:

all_pTags = soup.find_all('p')
# print list_of_pTags
# print len(listOfAllpTags)

for i in all_pTags:
    if 'www.sacd' in str(i):
        #         print i
        ind = all_pTags.index(i)

useful_pTags = all_pTags[ind+1:]
# print useful_pTags
# print type(useful_pTags[1])

# useful_pTags is a LIST of bs4.element.Tag objects


# In[68]:

text = []
for k in useful_pTags:
    text.append(k.get_text())

print text
# text is a list of strings (no <p> or any HTML tags in these strings)


# In[ ]:



