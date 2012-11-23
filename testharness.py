import json
import extract_features
import preprocess
from pprint import pprint

# A list of which features to use. 
# Right now the summary word bag is too bloated to use. Fixing that soon. (--john)
features_to_use = ['bill_feature_set'] # ['bill_features', 'summary_word_bag']



def load_json(filename):
    ''' Small helper to easily load json files '''
    return json.loads(open(filename).read())

def getBills(votes):
    '''
        Returns:
            List of bills associated with these votes
    '''
    bills = []
    vote_bill_map = load_json('vote_bill_map')
    for i, vote in enumerate(votes):
        if i % 100 == 0: print i
        vote_link = vote['vote']
        bill_id = vote_bill_map[vote_link]
        bill = load_json('bill_map/'+bill_id)
        bills.append(bill)
    return bills


def getData(rep_id, data_directory, preprocess_data=None):
    '''
        Loads any cached data from previous preprocessing to avoid time sinks. 
        Caches the final dataset for this rep under TrainingData/<rep_id>

        Returns:
            Training set for this rep in the form:
            { 'labels': A list of labels for each feature, 'data': List of data point objects}
    '''
    print 'Getting votes and bills...'
    votes = load_json(data_directory+'/'+rep_id) # Get the training votes for this rep
    bills = getBills(votes)
    print 'done.'

    # Generate information about the bills used for later feature generation
    if preprocess_data == None:
        preprocess_data = preprocess.preprocess(rep_id, bills, features_to_use)
    
    data_points = []
    all_labels = None
    label_hash = None

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
        if all_labels == None:
            all_labels = labels
        else:
            
            if labels != all_labels:
                print "Error: Labels differ on data points. Feature vector generation is messed up."

        data_points.append(point)

    # Save off the data and return 
    result = {'labels':labels, 'data':data_points}

    return result


def getTrainingData(rep_id):
    '''
        Get the training dataset for this rep.
        Note: Passing None to preprocess_data requests it to be regenerated for this set.
    '''
    return getData(rep_id, 'rep_votes_train', preprocess_data=None)


def getTestingData(rep_id):
    '''
        Get the test dataset for this rep
    '''
    pre_data = json.loads(open('preprocess_data/'+rep_id).read())
    return getData(rep_id, 'rep_votes_test', preprocess_data=pre_data)


#generates experiment data for single rep and stores in TrainingData/<rep_id>
def genExperimentData(rep_id):
    print ' ---- Generating Training Data ---- '
    # Save our training data
    train = getTrainingData(rep_id)
    f = open('data_set/main_train/'+rep_id, 'w')
    f.write(json.dumps(train))
    f.close()
    
    print
    print ' ---- Generating Testing Data ---- '

    # Save our test data
    test = getTestingData(rep_id)
    f = open('data_set/main_test/'+rep_id, 'w')
    f.write(json.dumps(test))
    f.close()
    
    
#generates experiment data for all reps and stores in TrainingData/<rep_id>
def genAllExperimentData():
    personlist = json.loads(open('representatives').read())

    for rep_id in personlist:
        genExperimentData(rep_id)
        

#generate exp data and store in folder ExperimentData/person/train[test]data
#for now only one feature set (0) [all features]
def trainSVM (person, experiment_name):
    train = load_json('data_set/'+experiment_name+'_train/'+person)
    test = load_json('data_set/'+experiment_name+'_test/'+person)

    # pass train to svm
    #test on test data
    pass
    #use scikit  and train on train data for each individual, then test on the
    # test set


#tests the classifier that predicts votes as yes if party of the rep is same as sponsor_party 
def baseline(person):
    pass


genExperimentData('400003')







