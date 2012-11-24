import numpy as np
import json
from sklearn import svm
from pprint import pprint
import operator



'''
When training an SVM with the Radial Basis Function (RBF) kernel, two parameters must be considered: C and gamma. 
The parameter C, common to all SVM kernels, trades off misclassification of training examples against simplicity of the decision surface.
 A low C makes the decision surface smooth, while a high C aims at classifying all training examples correctly. 
gamma defines how much influence a single training example has. The larger gamma is, the closer other examples must be to be affected.
'''



def getVoteOutcome(option):
    if option =="+":
        return 1
    else:
        return 0

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


def trainSVM(person,C,gamma, kernel, training_data_set):
    (train_data, data_labels) = genDataset(person, training_data_set)

    Xtrain=np.array(train_data)
    Ytrain= np.array(data_labels)
    classifier= svm.SVC(C=C,gamma=gamma, kernel=kernel)
    print classifier.fit (Xtrain,Ytrain)

    return classifier


def testSVM(person, classifier, test_data_set):
    (data, labels) = genDataset(person, test_data_set)

    test_data_length= len(labels)
    print "Length of test data is: "+str(test_data_length)
    test_data=np.array(data)
    data_labels= np.array(labels)
    prediction= classifier.predict(test_data)
    if len(prediction)!=test_data_length:
        print "Error in SVMtest: predicted data corrupted"
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
    print "Number of errors: "+str(numerrors)
    print "Error Percentage: "+ str(errorrate)
    print "Accuracy: " + str(accuracy)
    print "Number of false predictions of a yes vote: " + str(numfalseyes)
    print "Number of false predictions of a no vote: " + str(numfalseno)

    if classifier.kernel == 'linear':
        feature_weights = []
        # Print out the most heavlly weight features
        for i, ar in enumerate(classifier.coef_[0]):
            feature_weights.append((test_data_set['labels'][i], ar))

        feature_weights = sorted(feature_weights, key=operator.itemgetter(1), reverse=True)
        pprint(feature_weights[:40])


def svmLearn(person, C, gamma,kernel, experiment_name='main'):
    data_set_train = json.loads(open('data_set/'+experiment_name+'_train/'+str(person)).read()) # Ugly but short way to open training data
    data_set_test = json.loads(open('data_set/'+experiment_name+'_test/'+str(person)).read()) # Ugly but short way to open training data
                                                                                           # 
    classifier= trainSVM(person, C, gamma, kernel, data_set_train)
    testSVM(person, classifier, data_set_test)
    

svmLearn(400003, 1.0,0.0, 'linear')

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
