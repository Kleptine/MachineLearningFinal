import numpy as np
import json
from sklearn import svm



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

def genDataset(person, folderpath):
    path= "data_set/"
    f= open (folderpath+str(person))
    dict= json.loads(f.read())
    data_points= dict.get('data')
    traindata=[]
    data_labels=[]
    for point in data_points:
        traindata.append(point['vector'])
        voteobj= (point['vote_obj'])
        label= getVoteOutcome(voteobj['option'])
        data_labels.append(label)
    return (traindata, data_labels)


def trainSVM(person,C,gamma, kernel):
    path= "data_set/main_train/"
    (train_data, data_labels)= genDataset(person, path)

    Xtrain=np.array(train_data)
    Ytrain= np.array(data_labels)
    classifier= svm.SVC(C=C,gamma=gamma, kernel='rbf')
    print classifier.fit (Xtrain,Ytrain)
    return classifier


def testSVM(person, classifier):
    path= "data_set/main_test/"
    (data, labels)= genDataset(person, path)
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



def svmLearn(person, C, gamma,kernel):
    classifier= trainSVM(person, C, gamma, kernel)
    testSVM(person, classifier)

svmLearn(400003, 1.0,0.0, 'linear')
svmLearn(400003, 100.0,0.0,'linear')
svmLearn(400003, 10.0,0.001, 'rbf')
svmLearn(400003, 100.0,0.01, 'rbf')
svmLearn(400003, 100.0,0.001,'rbf')




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
