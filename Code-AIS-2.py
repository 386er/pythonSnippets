


import urllib2
import re
from xml.dom import minidom
import time
import pickle


september = {x: [ 0 for i in range(0,24)    ] for x in range(1,31)}
october   = {x: [ 0 for i in range(0,24)    ] for x in range(1,32)}


hdr = { 'User-Agent' : 'bot for seminar thesis project by 386er'}
pkl_file1 = open('redditlinklist.pkl', 'rb')
pkl_file2 = open('subredditlinklist.pkl', 'rb')
mainlinkindex = pickle.load(pkl_file1)
sublinkindex = pickle.load(pkl_file2)
comments = []

idindex = [entry[3] for entry in sublinkindex]
relevantlinks = [entry for entry in mainlinkindex if entry[3] not in idindex]            		  
mergeindex = sublinkindex + relevantlinks
bigthreads = [entry for entry in mergeindex if int(entry[2]) > 500]		  
smallthreads = [entry for entry in mergeindex if int(entry[2]) <= 500]
threads = []


for entry in smallthreads:
    try:
        threads.append(str(entry[0]))
    except UnicodeEncodeError:
        pass



def extractMonth(date):
    if date[17:20] == 'Sep':
        return 9
    elif date[17:20] == 'Oct':
        return 10
    else:
        return 0

def updateCount(month, day, hour):
    if month == 9:
        september[day][hour - 1] += 1
        return True		
    if month == 10:
        october[day][hour - 1] += 1
        return True		
    else:
        return False	

		
def storeComments(items):

##### Abschnitt für den Link

    linkdate = items[0].childNodes[3].toprettyxml()
    linkmonth = extractMonth(linkdate)
    linkday =  int(linkdate[14:16])
    linkhour = int(linkdate[26:28])

    updateCount(linkmonth, linkday, linkhour)

##### Abschnitt für die Comments #####
	
    for i in range(1, len(items)):

        commentdate = items[i].childNodes[3].toprettyxml()
        commentmonth = int(commentdate[14:16])
        commentday = int(commentdate[17:19])
        commenthour = int(commentdate[20:22])
        commenttext = items[i].childNodes[4].toprettyxml()[13:-15]

        updateCount(commentmonth, commentday, commenthour)

        if updateCount(commentmonth, commentday, commenthour) == True:
            comments.append(commenttext, commentmonth, commentday)	

			
			
for entry in threads:
    try:
        currentlink = entry   
        request = urllib2.Request( entry + ".xml?limit=500", headers = hdr)
        page = urllib2.urlopen(request)
        content = minidom.parseString(page.read())
        items = content.getElementsByTagName("item")
        storeComments(items)
        time.sleep(2.5)	
    except urllib2.HTTPError:
        pass
		
		
output1 = open('comments.pkl', 'wb')
pickle.dump(comments, output1)
output1.close()


output2 = open('september.pkl', 'wb')
pickle.dump(september, output2)
output2.close()		

output3 = open('october.pkl', 'wb')
pickle.dump(october, output3)
output3.close()			
	




