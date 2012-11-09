# Write some file here to generate a dataset from govtrack.us api
import httplib, json, glob

import sys
from pprint import pprint

oldest_congress = 0
limit = 1000

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
        
# Writes JSON object of rep IDs and rep dicts to representatives
def getReps2():
    votes = []
    conn = httplib.HTTPConnection('www.govtrack.us')
    for i in range(0,7):
        print i
        conn.request('GET', '/api/v1/person/?limit=2000&offset=' + str(i*2000))
        r2 = conn.getresponse()
        print r2.reason
        result = list(json.loads(r2.read())["objects"])
        if result != None:
            votes = votes + result
    reps = []
    for i in votes:
        role = i['current_role']
        if role != None:
            if role['role_type'] == 'representative':
                reps.append((i['id'], i))
    repsD = dict(reps)
    f = open('representatives','w')
    f.write(json.dumps(repsD))
    f.close()

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



def write_bills():

    conn = httplib.HTTPConnection('www.govtrack.us')
    

    # Get all votes on bills voted on for passage:
    conn.request('GET', '/api/v1/vote/?category=passage&limit='+str(limit))

    votePull = json.loads(conn.getresponse().read())

    allBills = []

    for v in votePull['objects']:
        allBills.append(v['related_bill'])

    while(votePull['meta']['next'] != None):
        conn.request('GET', votePull['meta']['next'])
        votePull = json.loads(conn.getresponse().read())

        for v in votePull['objects']:
            allBills.append(v['related_bill'])


        print str(len(allBills)) + '/' + str(votePull['meta']['total_count'])

    print 'generating bill map...'
    bill_map = {}
    for bill in allBills:
        if bill != None: # Some votes don't have associated bills because they're old and forgotten
            bill_map[bill['id']] = bill

    f = open('bills', 'w')
    f.write(json.dumps(bill_map))
    f.close()

    split_bills()

    f = open('bills', 'w')
    f.write(json.dumps(bill_map))
    f.close()

''' Splits bills file into parts for quick loading '''
def split_bills():
    print 'loading bills..'
    bills = json.loads(open('bills').read())

    print 'done.'

    for billid in bills:
        f = open('bill_map/'+str(billid), 'w')
        f.write(json.dumps(bills[billid]))
        f.close()

def generate_votes_per_rep():
    people = json.loads(open('representatives').read())

    conn = httplib.HTTPConnection('www.govtrack.us')

    billMap = {}

    for rep_id in sorted(people.keys())[202:]:
        print rep_id
        # Get all of rep's votes:
        conn.request('GET', '/api/v1/vote_voter/?person='+str(rep_id)+'&limit='+str(limit)+'&vote__congress__gte='+str(oldest_congress)+'&vote__category=passage')
        
        votePull = json.loads(conn.getresponse().read())
        allVotes = votePull['objects']

        while(votePull['meta']['next'] != None):
            conn.request('GET', votePull['meta']['next'])
            votePull = json.loads(conn.getresponse().read())

            allVotes.extend(votePull['objects'])

            print str(len(allVotes)) + '/' + str(votePull['meta']['total_count'])

        f = open('rep_votes_map/'+str(rep_id),'w')
        f.write(json.dumps(allVotes))
        f.close()

generate_votes_per_rep()