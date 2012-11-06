#
#   Extract features from a given bill object
import httplib, json

import sys
from pprint import pprint
dictj={}
reps=[]


def extractFeatures(bill):
    return {} # Return dictionary of features

# TODO /--------------------------------------------------------------------------------------
# Gets the training set for a person given a person object and a list of all bills
def getInputVectors(person, billMap):
    
    return []


#get all representatives, high limit gets all - verified (jisha) 
#not used currently 
def getPeople():
    connpeople = httplib.HTTPConnection('www.govtrack.us')
    connpeople.request('GET', '/api/v1/person/?limit=1000')
    r = connpeople.getresponse() 
    people= json.loads(r.read())["objects"] 
    #print people
    for person in people:
        print person["id"]
        getVotes(person["id"])

# Returns a list of current representative IDs
def getReps():
    votes = []
    conn = httplib.HTTPConnection('www.govtrack.us')
    for i in range(0,7):
        #print i
        conn.request('GET', '/api/v1/person/?limit=2000&offset=' + str(i*2000))
        r2 = conn.getresponse()
        #print r2.reason
        text= r2.read()
        try:
            repstext= json.loads(text)
            result = list(repstext["objects"])
            if result != None:
                votes = votes + result
        except:
            print "Unexpected error in getReps()", sys.exc_info()[0]         
            f= open("testReps.txt","w")
            f.write(text)
    reps = []
    count = 0
    for i in votes:
        role = i['current_role']
        if role != None:
            if role['role_type'] == 'representative':
                count = count + 1
                reps.append(i['id'])
    return reps

def getAllVotes():
    global reps
    reps= getReps()
    print reps
    for rep in reps:
        getVotes(rep)

#Getting bills also fails when limit is above 6000 (5000 works) which makes me think this may not be an issue with
# large size of data coz one api call(votes) fails at 12000 and the other(bills) at 6000. (jisha)

#edit
# Votes: I did some ordering giving highest limit and looks like representatives have not voted on bills with ids(display id in link) above 600 hmm ?
# Bills: tried ordering in descending order of introduced_date (changing the limit from 1000 to 5000 has no effect on the data )
#the highest bill  id returned is 6578 - there are missing ids though which explains the limit of 1000/5000 working?: 
#by     http://www.govtrack.us/api/v1/bill/?limit=1000&congress=112&order_by=-introduced_date 

#setting a high limit should get all acc to documentation, but fails at limit=12000 (11000 works)
#puts the list of votes by this person in a file (temp)
def getVotes (person= None):
    allvotes=[]
    global dictj
    conn = httplib.HTTPConnection('www.govtrack.us')
    for i in range(1,10):
        conn.request('GET', '/api/v1/vote_voter/?person='+str(person)+'&offset='+str(i*1000)+'&congress=112&limit=1000&order_by=-created')
        r1 = conn.getresponse()
        print r1.reason
        text= r1.read()
        #bills = json.loads(r1.read()) 
        #ft.write(text)
        #ft.close()
        try:
            allbills = json.loads(text)
            bills= allbills["objects"]
            for bill in bills:
                print bill
                allvotes.append(bill)
                dictj[person]=bill["link"] #TODO store tuple of (id of bill extracted from link , option)
        except:
             print "Unexpected error in getVotes", sys.exc_info()[0]
             ft= open("test.txt","w")
             print "Person is= "+ str(person)
             ft= open("test.txt","w")
             ft.write(text)
    f= open("votes"+person+".txt",'w')
    f.write(json.dumps(allvotes))
        
    #pprint (json.dumps(bills))
getAllVotes()
