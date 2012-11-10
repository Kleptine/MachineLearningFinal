
#
#   Extract features from a given bill object
import httplib, json, re

import sys
from pprint import pprint
dictj={}
reps=[]

def get_bill(id):
    f = open('bill_map/'+str(id))
    return json.loads(f.read())

def extractFeatures(bill):
    '''
    Returns:
        Dictionary of features representing this bill
    '''

    # Clean up name (remove dates)
    name = bill['sponsor']['name']
    match = re.search('[^\[]*', name)
    clean_name = name[match.start():match.end()].replace(' ','')
    print clean_name

    year = int(bill['current_status_date'][0:4])
    year_mod2 = int(bill['current_status_date'][0:4]) % 2
    year_mod4 = int(bill['current_status_date'][0:4]) % 4
    year_mod6 = int(bill['current_status_date'][0:4]) % 6
    year_introduced = int(bill['introduced_date'][0:4])

    bill_length = year - year_introduced

    sponsor_end_year = int(bill['sponsor_role']['enddate'][:4])
    sponsor_start_year = int(bill['sponsor_role']['startdate'][:4])
    sponsor_gender = bill['sponsor']['gender']
    sponsor_is_alive = bill['is_current']

    sponsor_has_nickname = (bill['sponsor']['nickname'] != '')

    congress = int(bill['congress'])



    features = {
        'sponsor_name': clean_name,
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
        'bill_length': bill_length,
        'sponsor_end_year': sponsor_end_year,
        'sponsor_start_year': sponsor_start_year,
        'sponsor_gender': sponsor_gender,
        'sponsor_is_alive': sponsor_is_alive,
        'sponsor_has_nickname': sponsor_has_nickname,
        'congress': congress
    }


    return features # Return dictionary of features


def generateFeatureVector(bill_id):
    #extractFeatures...
    return


# TODO /--------------------------------------------------------------------------------------
# Gets the training set for a person given a person object and a list of all bills
def getInputVectors(person, billMap):    
    return []


bill = get_bill(75622)

pprint(extractFeatures(bill))