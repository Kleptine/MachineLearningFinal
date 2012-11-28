import numpy as np
import json
from sklearn import svm
from pprint import pprint
import operator
import sys
import os.path
import json
import config 
import scipy.sparse
import time
import sklearn.preprocessing as preprocessing
import heapq

'''
When training an SVM with the Radial Basis Function (RBF) kernel, two parameters must be considered: C and gamma. 
The parameter C, common to all SVM kernels, trades off misclassification of training examples against simplicity of the decision surface.
 A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly. 
gamma defines how much influence a single training example has. The larger gamma is, the closer other examples must be to be affected.
'''


def getVoteOutcome(option):
    if option =="+":
        return 1
    elif option == "-":
        return 0

    raise "ERROR: ABSTAIN VOTE COUNTED"


def genDataset(person, data_set):
    '''
        Generate the data to plug into the SVM
    '''

    data_points = data_set['data']
    
    traindata=[]
    data_labels=[]
    for point in data_points:
        traindata.append(point['vector'])
        voteobj= (point['vote_obj'])
        label= getVoteOutcome(voteobj['option'])
        data_labels.append(label)
    return (traindata, data_labels)


def trainSVM(person,C,gamma, kernel, training_data_set, debug=2):
    '''
        Args:
            debug: How much info to print: 0=none, 1=minimal, 2=all
    '''
    (train_data, data_labels) = genDataset(person, training_data_set)

    Xtrain=np.array(train_data)
    Ytrain=np.array(data_labels)

    if debug >= 1: print "Sample length: " + str(len(Xtrain))
    if debug >= 2: print "Training SVM for C = "+ str(C) +", kernel= "+kernel

    if config.normalize_data:
        # Create a new scaler object so we can apply the same scale to the test set
        if config.normalize_type == 'center':
            #BAD PRACTICE: But I'm lazy and don't want to pass around tranformation objects
            config.scaler = preprocessing.Scaler().fit(Xtrain)
        if config.normalize_type == 'unit_length':
            config.scaler = preprocessing.Normalizer().fit(Xtrain)

        Xtrain = config.scaler.transform(Xtrain)


    # Convert to sparse representation if requested
    if config.use_sparse_data:
        print "Booyy, we makin this sparse!"
        Xtrain =scipy.sparse.csr_matrix(Xtrain)
    if config.classifier==0:
        classifier= svm.SVC(C=C,gamma=gamma, kernel=kernel, cache_size=1000)
    else:
        classifier= tree.DecisionTreeClassifier()

    sys.stdout.write('.Learning.')
    start = time.time()
    classifier.fit(Xtrain,Ytrain)
    end = time.time()
    sys.stdout.write('..done\n')
    print "Took "+str(end-start) + " seconds."

    trainAcc = classifier.score(Xtrain, Ytrain)
    stats = {
        'Train Accuracy': trainAcc,
        'Train Size': len(train_data)
    }

    return (classifier, stats)


def testSVM(person, classifier, test_data_set, debug=2):
    '''
        Args:
            debug: How much info to print: 0=none, 1=minimal, 2=all
    '''
    # Get our data and our classes
    (data, labels) = genDataset(person, test_data_set)

    test_data_length= len(data)
    if debug >= 2: print "Test Data Length: "+str(test_data_length)

    # Convert our data into something useable by the SVM library
    test_data=np.array(data)
    data_labels= np.array(labels)

    # Scale data if necessary
    if config.normalize_data:
        test_data = config.scaler.transform(test_data)


    # PREDICT IT!
    if config.validate:
        if debug >= 2: print "Testing SVM on Validation Set "
    else:
         if debug >= 2: print "Testing SVM Classiier"
    prediction= classifier.predict(test_data)

    if len(prediction)!=test_data_length:
        print "Error in SVMtest: Predicted labels not same length as test data."
        return


    # Grade our results:
    stats = {}  # Dictionary to store statistics

    numerrors=0
    numfalseyes=0
    numfalseno=0
    for i in range(0,test_data_length):
        if data_labels[i]==0:
            if prediction[i]==1:
                numerrors=numerrors+1
                numfalseyes = numfalseyes+1
        else:
            if prediction[i]==0:
                numerrors=numerrors+1
                numfalseno = numfalseno+1
    errorrate= float(numerrors)/float(test_data_length)*100
    accuracy= float(100)- errorrate
    if debug >= 2: print "Number of errors: "+str(numerrors)
    if debug >= 1: print "Error Percentage: "+ str(errorrate)
    if debug >= 1: print "Accuracy: " + str(accuracy)
    if debug >= 2: print "Number of false predictions of a yes vote: " + str(numfalseyes)
    if debug >= 2: print "Number of false predictions of a no vote: " + str(numfalseno)
    stats['Test Errors'] = numerrors
    stats['Test Accuracy'] = accuracy
    stats['Test Error Rate'] = errorrate
    stats['Test False Positives'] = numfalseyes
    stats['Test False Negatives'] = numfalseno
    stats['Test Size'] = str(test_data_length)


    # Print out the most heavily weight features (only defined for a linear kernel)
    if debug >= 2 and classifier.kernel == 'linear':
        print 
        print "Top weighted features:"
        feature_weights = []
        # Form a tuple list so we can sort the list by feature weight
        for i, ar in enumerate(classifier.coef_[0]):
            if test_data_set['labels'][i][:4] != 'Rep.' and test_data_set['labels'][i][:4] != 'Sen.':
                feature_weights.append((test_data_set['labels'][i], abs(ar), ar))

        feature_weights = sorted(feature_weights, key=operator.itemgetter(1), reverse=True)

        # The middle of the tuple is the absolute value used for sorting, remove that and display
        for feature_name, _, value in feature_weights:
            pprint((value, feature_name))

    return stats




def svmLearn(person, C=1.0, gamma=0.0 , kernel='linear', experiment_name='main', debug=2,Clist=[1.0],kernelList=['linear']):
    print 'data_set/'+experiment_name+'_train/'+str(person)
    data_set_train = json.loads(open('data_set/'+experiment_name+'_train/'+str(person)).read()) # Ugly but short way to open training data
    data_set_validation=[]
    data_set_test = json.loads(open('data_set/'+experiment_name+'_test/'+str(person)).read()) # Ugly but short way to open test data

    if debug >= 1: 
        print
        print ' ---- Training / Classifying ---- '

    if config.validate:
        svmstats={}
        data_set_validation = json.loads(open('data_set/'+experiment_name+'_validation/'+str(person)).read()) # Ugly but short way to open test data
        for kernelval in kernelList:
            for Cvalidate in Clist: #change
                classifier, train_stats = trainSVM(person, Cvalidate, gamma, kernelval, data_set_train, debug)
                validation_stats = testSVM(person, classifier, data_set_validation, debug)
                acc=(validation_stats['Test Accuracy'])
                stats = {}
                stats.update(train_stats)
                stats.update(validation_stats)
                svmstats[acc] = (stats, C)
        print svmstats
        bestAccuracy=(heapq.nlargest(1,svmstats.keys()))[0]
        (bestStats,bestC)= svmstats.get(bestAccuracy)
        if debug >= 2:
            print "best C Value for SVM is " + str(C)
        return bestStats


    else:
        classifier, train_stats = trainSVM(person, C, gamma, kernel, data_set_train, debug)
        test_stats = testSVM(person, classifier, data_set_test, debug)
        stats = {}
        stats.update(train_stats)
        stats.update(test_stats)

        return stats


def svmLearnAll(C=1.0, gamma=0.0 , kernel='linear', experiment_name='main', debug=2, rep_max=None, Clist=[1.0],kernelList=['kernel']):
    personlist = json.loads(open('representatives').read())
    if rep_max == None: 
        rep_max = len(personlist.keys())
    # Keep a record of everyone's statistics
    all_stats = {}

    start = time.time()

    count = 0
    for rep_id in personlist.keys()[:rep_max]:
        print 
        print '====================================='
        print '     '+rep_id+'    '+str(count)+'/'+str(len(personlist))
        print
        stats = svmLearn(rep_id, C=C, gamma=gamma, kernel=kernel, experiment_name=experiment_name, debug=debug, Clist=Clist, kernelList=kernelList)
        all_stats[rep_id] = stats

        count += 1

    end = time.time()

    acc = 0
    tot = 0
    for s in all_stats:
        acc += int(all_stats[s]['Test Errors'])
        tot += int(all_stats[s]['Test Size'])
    acc = float(acc)/float(tot)

    print
    print  'Total time:   '+str(end-start) + '  seconds.'
    print  'Total Accuracy:   '+str(1-acc)
    print

    return all_stats


# Call this from an experiment such as exp__no_summary.py
#svmLearn(400003, C=1.0, gamma=0.0, kernel='linear', debug=1)

#svmLearn(412282, 1.0,0.0, 'linear')

#svmLearn(400003, 100.0,0.0,'linear')
#svmLearn(400003, 10.0,0.001, 'rbf')
#svmLearn(400003, 100.0,0.01, 'rbf')
#svmLearn(400003, 100.0,0.001,'rbf')




'''
X= np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
Y=np.array([-1,0,1])
test=np.array([[1,2,3,4],[1,6,7,8],[1,10,11,12]])


svmkernel = svm.SVC(kernel='rbf')
clf = svm.SVC(gamma=0.001, C=100.)
svc = svm.SVC(kernel='linear')
print clf.fit(X,Y)
print clf.predict(test)
'''
