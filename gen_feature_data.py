import json
import extract_features
import preprocess
import config
from pprint import pprint
import os.path
import sys

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
        preprocess_data = preprocess.preprocess(rep_id, bills)
    
    data_points = []
    all_labels = None
    label_hash = None

    print "Generating all feature vectors"

    # Iterate through all the votes and bills and compile the final data set
    for i, v in enumerate(votes):
        if i % 20 == 0: 
            a_string = str(int(float(i)/float(len(votes))*100))+'%'
            sys.stdout.write('\b%s%s'%(a_string,'\b' * len(a_string))) # '\b' erases a char

        # Our final point object to feed into training. woo
        point = {
            'option': v['option'],
            'bill': bills[i],
            'vote_obj': v
        }

        # Generate the input vector for this vote
        vector, labels = extract_features.generate_feature_vector(point['bill'], preprocess_data)
        point['vector'] = vector

        # If the labels for this vector are different from the previous, 
        # the feature generation is messed up or out of order
        if all_labels == None:
            all_labels = labels
        else:
            
            if labels != all_labels:
                print "Error: Labels differ on data points. Feature vector generation is messed up."

        # Ignore abstaining votes
        if point['option']=="+" or point['option']=="-" or config.remove_abstaining_votes == False:
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


#generates experiment data for single rep and stores in data_set/<experiment_name>_(train/test)/<rep_id>
def genExperimentData(rep_id, experiment_name):

    print
    print "-------- " + rep_id + ' --------'
    print 

    print ' ---- Generating Training Data ---- '
    # Get our training data
    train = getTrainingData(rep_id)

    # Create vector directory to save if necessary
    if not os.path.exists('data_set/'+experiment_name+'_train'):
        os.makedirs('data_set/'+experiment_name+'_train')

    f = open('data_set/'+experiment_name+'_train/'+rep_id, 'w')
    f.write(json.dumps(train))
    f.close()
    

    print
    print ' ---- Generating Testing Data ---- '
    # Save our test data
    test = getTestingData(rep_id)

    if not os.path.exists('data_set/'+experiment_name+'_test'):
        os.makedirs('data_set/'+experiment_name+'_test')

    f = open('data_set/'+experiment_name+'_test/'+rep_id, 'w')
    f.write(json.dumps(test))
    f.close()
    
    
#generates experiment data for all reps and stores in TrainingData/<rep_id>
def genAllExperimentData(experiment_name):
    personlist = json.loads(open('representatives').read())

    for rep_id in personlist:
        genExperimentData(rep_id, experiment_name)






