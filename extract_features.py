#   Extract features from a given bill object

import sys, httplib, json, re
import glob
from pprint import pprint
dictj={}
reps=[]
nameID=-1

def get_bill(id):
    f = open('bill_map/'+str(id))
    return json.loads(f.read())

def boolToInt(bool):
    if bool:
        1
    else:
        0
        
def genderToInt(gender):
    if gender==None or ( not (isinstance(gender,str))):
        2
    elif gender.lower()== 'male':
        1
    else:
        0
        
def partyToInt(party):
    if party==None or ( not (isinstance(party,str))):
        2
    elif (party.lower()=="democrat"):
        1
    else:
        0
        
def getStringVectors(dict, num,field):
    billFeatures=[]
    for billFeat in dict:
        newdict={}
        for (k,v) in billFeat.items():
            if v==None:
                continue
            elif k==field:
                vector= [0] * (num+1)
                vector[v]=1
                newdict[k]= vector
            else:
                newdict[k]=v
        billFeatures.append(newdict)
    return billFeatures      
    

def extractFeatures(bill, nameID,districtID, names, districts): #start with -1
    '''
    Returns:
        Dictionary of features representing this bill
    '''
  
    # Clean up name (remove dates)
    name = (bill['sponsor'])['name']
    sponsor_district= bill['sponsor_role']['district']
    match = re.search('[^\[]*', name)
    clean_name = name[match.start():match.end()].replace(' ','')
    if clean_name in name:
        print "Repeated name: " + clean_name 
        nameID= names[clean_name]
    else:
        nameID=nameID+1
        names[clean_name]= nameID
        
    if sponsor_district in districts:
        print "Repeated district " + str(sponsor_district) 
        districtID= districts[sponsor_district]
    else:
        districtID=districtID+1
        names[sponsor_district]= districtID
        
    year = int(bill['current_status_date'][0:4])
    year_mod2 = int(bill['current_status_date'][0:4]) % 2
    year_mod4 = int(bill['current_status_date'][0:4]) % 4
    year_mod6 = int(bill['current_status_date'][0:4]) % 6
    year_introduced = int(bill['introduced_date'][0:4])

    bill_is_alive = boolToInt(bill['is_alive'])
    bill_is_current = boolToInt(bill['is_current'])

    bill_length = year - year_introduced

    sponsor_end_year = int(bill['sponsor_role']['enddate'][:4])
    sponsor_start_year = int(bill['sponsor_role']['startdate'][:4])
    sponsor_gender = genderToInt(bill['sponsor']['gender'])

                    
   
    sponsor_party= partyToInt(bill['sponsor_role']['party'])
    #sponsor_role_type= bill['sponsor_role']['role_type']

    sponsor_has_nickname = boolToInt(bill['sponsor']['nickname'] != '')
    sponsor_has_twitter= boolToInt(bill['sponsor']['twitterid']!='')

    congress = int(bill['congress'])



    features = {
        'sponsor_name': nameID,
        #'sponsor_name_first': bill['sponsor']['firstname'],
        #'sponsor_name_middle': bill['sponsor']['middlename'],
        #'sponsor_name_last': bill['sponsor']['lastname'],
        'vote_year': int(bill['current_status_date'][0:4]),
        'vote_month': int(bill['current_status_date'][5:7]),
        'vote_day': int(bill['current_status_date'][9:]),
        'vote_year_m2': year_mod2,
        'vote_year_m2': year_mod4,
        'vote_year_m2': year_mod6,
        'year_introduced': year_introduced,
        'bill_is_alive' : bill_is_alive,
        'bill_is_current': bill_is_current,
        'bill_length': bill_length,
        'sponsor_end_year': sponsor_end_year,
        'sponsor_start_year': sponsor_start_year,
        'sponsor_gender': sponsor_gender,
        'sponsor_district':sponsor_district,
        'sponsor_party':sponsor_party,
        'sponsor_has_nickname': sponsor_has_nickname,
        'sponsor_has_twitter': sponsor_has_twitter,
        'congress': congress
    }
    return (features, nameID,districtID, names, districts)
   


# TODO /--------------------------------------------------------------------------------------
# Gets the training set for a person given a person object and a list of all bills
def getInputVectors(person):  #taking in a billmap for now
    f= open("./voting_records/"+str(person),"r")
    billsdict=json.loads(f.read()) 
    bills=billsdict.keys()
    billFeatures=[]
    names={}
    districts={}
    nameID= -1
    districtID= -1
    for bill in bills:
        b= open("./bill_map/"+str(bill),"r")
        dictrictID=districtID+1
        text= json.loads(b.read())
        (dict,nameID,districtID,names, districts)= extractFeatures(text,nameID, districtID,names, districts)
        billFeatures. append(dict)         
    numNames= nameID
    numdistricts= districtID
    billFeatures= getStringVectors(billFeatures,nameID, "sponsor_name")
    billFeatures= getStringVectors(billFeatures,nameID, "sponsor_district")
    file= open("./TrainingData/"+str(person),"w")
    file.write(json.dumps(billFeatures))
    return billFeatures
        
# takes in list of people and generates list of feature vectors for bills each person voted on      
def getAllData():
    reps = open('representatives')
    dictr = json.loads(reps.read())
    for key in dictr:
        getInputVectors(key)
            
            

getInputVectors(400003)
#getAllData()
#pprint(extractFeatures(bill))