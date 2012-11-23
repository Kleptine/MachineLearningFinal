import json
import extract_features
import preprocess
from pprint import pprint
# This file basically makes use of our databases to train a single rep.
# Train a single rep

repId = '400003'
features_to_use = ['bill_feature_set'] # ['bill_features', 'summary_word_bag']



def getTrainVotes(rep_id):
    ''' Gets this rep's votes '''
    return load_json('rep_votes_train/'+rep_id)

def getBills(rep_id, votes):
    bills = []
    vote_bill_map = load_json('vote_bill_map')
    for i, vote in enumerate(votes):
        if i % 100 == 0: print i
        vote_link = vote['vote']
        bill_id = vote_bill_map[vote_link]
        bill = load_json('bill_map/'+bill_id)
        bills.append(bill)
    return bills

def getTrainingPoints(rep_id):
    print 'Getting votes and bills...'
    votes = getTrainVotes(rep_id)
    bills = getBills(rep_id, votes)
    print 'done.'

    # Generate information about the bills used for later feature generation
    preprocess_data = preprocess.preprocess(rep_id, bills, features_to_use)
    data_points = []
    all_labels = None

    print "Generating all feature vectors"
    # Iterate through all the votes and bills and compile the final data set
    for i, v in enumerate(votes):
        if i % 200 == 0: print '%i / %i' % (i, len(votes))

        # Our final point object to feed into training. woo
        point = {
            'option': v['option'],
            'bill': bills[i],
            'vote_obj': v
        }

        # Generate the input vector for this vote
        vector, labels = extract_features.generate_feature_vector(point['bill'], preprocess_data, features_to_use)
        point['vector'] = vector

        # If the labels for this vector are different from the previous, 
        # the feature generation is messed up or out of order
        

        data_points.append(point)

    return data_points


def load_json(filename):
    return json.loads(open(filename).read())

points = getTrainingPoints(repId)
f = open('__testpoints', 'w')
f.write(json.dumps(points[:10]))
f.close()