import sys
import json
import random

#dictionary of feature combinations
featurelistids={}
featurelistids["0"]=["sponsor_party","sponsor_district"]
featurelistids["1"]=["sponsor_party"]

def addfeaturelist():
    pass

#returns a tuple of train and test data after dividing into train/test ratio r/100-r
#saves the train and test data in filepath + "train/text"
def divide( r= 70, datalist=None, filepath=None):
    totallen= len(dataset)
    numtrain= (float(r)/float(100-r)) * float(totallen) 
    traindata=[]
    testdata=[]
    for data in datalist:
        randint=random.randint(1,100)
        if (randint<=r) and n<numtrain:
            traindata.append(data)
            n=n+1
        else:
            testdata.append(data)
    print "length of train text is "+ str(len(traindata))
    print "length of test text is "+str(len(testdata))
    train= open(filepath+"train","w") #acc to requirements
    test= open(filepath+"test","w")
    train.write(json.dumps(traindata))
    test.write(json.dumps(testdata))
    return (traindata, testdata)

#divides into train/text, converts feature dictionaries into train and test data format
#saves the train and test feature dictionaries as [person]train and [person]test in Training Data folder
#converts into format for experiments and stores in filepath+ traindata/testdata
def getData(featurelist,person, filepath):
    text= open ("TrainingData/"+str(person),"r")
     #for different features, since we're trying different feature sets first 
    (traintext,testtext)= divide(datalist= json.loads(text), filepath="TrainingData/"+str(person)) #dividing into train and test
    f1=open(filepath+"traindata","w")
    f2=open(filepath+"testdata","w")
    train=[]
    text=[]
    #flatten the list with needed features only
    for element in train:
        dict={}
        for feature in featurelist:
            dict[feature]=element[feature]
        print dict
        train.append(dict.values)

    for element in test:
        dict={}
        for feature in featurelist:
            dict[feature]=element[feature]
        print dict
        test.append(dict.values) 
    train=sum(train,[]) #flattens the list
    test=sum(test,[])   
    f1.write(json.dumps(train))
    f2.write(json.dumps(test))


#tests the classifier that predicts votes as yes if party of the rep is same as sponsor_party 
def baseline(person):
    pass


#generates experiment data for all reps in stores in folder ExperimentData/[1]/[person]
#featurelistnum represents which featurecombination we are trying
def getAllExperimentData(personlist=None, featurelist=None,featurelistnum=0):
    for person in personlist:
        getData(featureList=None, person=person, filepath = "ExperimentData/"+str(featurelistnum)+str(person)+"/")


#generate exp data and store in folder ExperimentData/person/train[test]data
#for now only one feature set (0) [all features]
def trainSVM (person):
    tr= open ("ExperimentData/0/"+str(person)+"/traindata","r") #for different 
    te= open ("ExperimentData/0/"+str(person)+"/testdata","r") 
    train= json.loads(tr)
    test= json.loads(te)

    # pass train to svm
    #test on test data
    pass
    #use scikit  and train on train data for each individual, then test on the
    # test set







