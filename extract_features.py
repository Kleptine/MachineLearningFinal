#
#   Extract features from a given bill object

import httplib, json
from pprint import pprint
dict={}


def extractFeatures(bill):
    return {} # Return dictionary of features

# TODO /--------------------------------------------------------------------------------------
# Gets the training set for a person given a person object and a list of all bills
def getInputVectors(person, billMap):
    
    return []


#get all representatives, high limit gets all - verified (jisha)
def getPeople():
    connpeople = httplib.HTTPConnection('www.govtrack.us')
    connpeople.request('GET', '/api/v1/person/?limit=1000')
    r = connpeople.getresponse() 
    people= json.loads(r.read())["objects"] 
    #print people
    for person in people:
        print person["id"]
        getVotes(person["id"])



#Getting bills also fails when limit is above 6000 (5000 works) which makes me think this may not be an issue with
# large size of data coz one api call(votes) fails at 12000 and the other(bills) at 6000. (jisha)

#edit
# Votes: I did some ordering giving highest limit and looks like representatives have not voted on bills with ids(display id in link) above 600 hmm ?
# Bills: tried ordering in descending order of introduced_date (changing the limit from 1000 to 5000 has no effect on the data )
#the highest bill  id returned is 6578 - there are missing ids though which explains the limit of 1000/5000 working?: 
#by     http://www.govtrack.us/api/v1/bill/?limit=1000&congress=112&order_by=-introduced_date 

#haven't written al files yet, had an error 

#setting a high limit should get all acc to documentation, but fails at limit=12000 (11000 works)
#puts the list of votes by this person in a file (temp)
def getVotes (person= None):
    global dict
    conn = httplib.HTTPConnection('www.govtrack.us')
    conn.request('GET', '/api/v1/vote_voter/?person='+person+'&congress=112&limit=11000&order_by=-created')
    r1 = conn.getresponse()
    
    print r1.reason
    #bills = json.loads(r1.read())
    bills = json.loads(r1.read())["objects"]
    for bill in bills:
        dict[person]=bill["link"] #TODO store tuple of (id of bill extracted from link , option)
    f= open("votes"+person+".txt",'w')
    f.write(json.dumps(bills))
    #pprint (json.dumps(bills))
    
    
getPeople()