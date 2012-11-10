import httplib, json, glob

def extractVotes(repId):
    outDictionary = dict()
    outList = []
    f = open('rep_votes_map/' + str(repId),'r')
    votes = json.loads(f.read())
    print len(votes)
    conn = httplib.HTTPConnection('www.govtrack.us')
    bill_map = open('vote_bill_map', 'r')
    bmapping = json.loads(bill_map)
    f.close()
    for vote in votes:
        voteId = vote.vote
        voteH = '/api/v1/vote/' + str(voteId)
        billId = bmapping.voteH
        decision = vote.option
        print billId
        outList.append((billId,decision))
    outDictionary = dict(outList)
    outFile = open('voting_records/' + str(repId), 'w')
    outFile.write(json.dumps(outDictionary))
extractVotes(400003)
    