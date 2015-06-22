import urllib2
import re
from xml.dom import minidom
import time
import pickle


# All subreddits that are shown on the search site

subreddits = ["POLITIC","politics", "ModerationLog", "AdviceAnimals", "AskReddit", "conspiro", "funny", "conspiracy",
"PoliticalDiscussion","Libertarian","circlejerk","Conservative","news","reddit.com","PoliticalHumor", "fringediscussion",
"Ask_Politics","pics","progressive","uspolitics" ]
linkindex = []; sublinkindex = []
hdr = { 'User-Agent' : 'bot for seminar thesis project by 386er'}


def getLinksFromPage(items, linkindex):
    for i in range(0, len(items)):

        link = items[i].childNodes[1].toprettyxml()[6:-8]  #  Link zu den Comments 
        date = str(items[i].childNodes[3].toprettyxml()[9:-11]) #  Erstelldatum des Links
        description = items[i].childNodes[4].toprettyxml()      #  Beschreibung zum Link
        if re.search(r'\[[0-9]+ comments\]', description):      #  In der Beschreibung ist die Anzahl der Links gespeichert
            match = re.search(r'\[[0-9]+ comments\]', description)
            comments = str(match.group(0)[1:-10])
        else:
            comments = '0'    
        linkid = str(link[link.find("/comments/") + 10 : link.find("/comments/") + 16])

        if ('government' and 'shut' and 'down' in link ) or ('government' and 'shut' and 'down' in description):		
            linkindex.append((link, date ,comments ,linkid))


##### Links aus main search results

request = urllib2.Request("http://www.reddit.com/search.xml?q=government_shutdown&sort=relevance&t=year&limit=100", headers = hdr)
page = urllib2.urlopen(request)
content = minidom.parseString(page.read())
items = content.getElementsByTagName("item")

while len(items) >= 100:

    getLinksFromPage(items, linkindex)

    request = urllib2.Request("http://www.reddit.com/search.xml?q=government_shutdown&sort=relevance&t=year&limit=100&count=" + str(count) + "&after=t3_" + linkindex[-1][3], headers = hdr)
    page = urllib2.urlopen(request)
    count += 100
    content = minidom.parseString(page.read())
    items = content.getElementsByTagName("item")
    time.sleep(2.5)

getLinksFromPage(items, linkindex)



			
##### Links aus den Subreddits ######			

for subreddit in subreddits:			
	
    count = 100	
    request = urllib2.Request("http://www.reddit.com/r/" + subreddit + "/search.xml?q=government_shutdown&sort=relevance&limit=100&restrict_sr=on&t=year", headers = hdr)
    page = urllib2.urlopen(request)
    content = minidom.parseString(page.read())
    items = content.getElementsByTagName("item")
		
    while len(items) >= 100:

        getLinksFromPage(items, sublinkindex)

        request = urllib2.Request("http://www.reddit.com/r/" + subreddit +  "/search.xml?q=government_shutdown&sort=relevance&restrict_sr=on&t=year&limit=100&count=" + str(count) + "&after=t3_" + linkindex[-1][3], headers = hdr)
        page = urllib2.urlopen(request)
        count += 100
        content = minidom.parseString(page.read())
        items = content.getElementsByTagName("item")
        time.sleep(2.5)

    getLinksFromPage(items, sublinkindex)


output1 = open('subredditlinklist.pkl', 'wb')
pickle.dump(sublinkindex, output)
output1.close()	

outpu2 = open('redditlinklist.pkl', 'wb')
pickle.dump(linkindex, output)
output2.close()
