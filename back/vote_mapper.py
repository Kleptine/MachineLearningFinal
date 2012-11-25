import httplib, json, glob

def extractVotes(repId):
    outDictionary = dict()
    outList = []
    f = open('rep_votes_map/' + str(repId),'r')
    votes = json.loads(f.read())
    f.close()
    billMap = json.loads((open('vote_bill_map')).read())
    for vote in votes:
        voteId = vote['vote']
        billId = billMap[voteId]
        decision = vote['option']
        if decision == '+':
            outList.append((billId,1))
        elif decision == '-':
            outList.append((billId,0))
    outDictionary = dict(outList)
    if len(votes) == 0:
        print repId
    outFile = open('voting_records/' + str(repId), 'w')
    outFile.write(json.dumps(outDictionary))

reps = open('representatives')
dictr = json.loads(reps.read())
for key in dictr:
    extractVotes(key)
    
    