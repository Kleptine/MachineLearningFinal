import gen_feature_data
import svm
import config
from gen_feature_data import load_json
import json
import sys
import time

'''
Baseline: Reps vote yes for bills sponsored by the same party
'''

name = "Baseline"

def baseline(person, debug=1):
    rep_data = load_json('representatives')[person]
    rep_party = (rep_data['current_role'])['party']
    path= "all_no_summary_linear_"
    #using data from all_no_summary_linear experiment coz data for all reps is generated 

    data_set_test = json.loads(open('data_set/'+path+'test/'+str(person)).read()) # Ugly but short way to open test data
    test_data_points = data_set_test['data']
    data_points = test_data_points #concatenating train and test datasets
    dataset_length = len(data_points)

    numerrors=0
    numfalseyes=0
    numfalseno=0

    stats={}
    
    for point in data_points:
        sponsor_party=((point['bill'])['sponsor_role'])['party']
        #print sponsor_party
        voteobj= (point['vote_obj'])
        vote= svm.getVoteOutcome(voteobj['option'])

        #predict vote based on sponsor_party
        predictedVote= 0
        if rep_party== sponsor_party:
            predictedVote=1

        #evaluate performance
        if vote==0:
            if predictedVote==1:
                numerrors=numerrors+1
                numfalseyes = numfalseyes+1
        else:
            if predictedVote==0:
                numerrors=numerrors+1
                numfalseno = numfalseno+1

    errorrate= float(numerrors)/float(dataset_length)*100
    accuracy= float(100)- errorrate
    print
    print '====================================='
    print '       '+name
    print '====================================='
    print 
    if debug >= 2: print "Number of errors: "+str(numerrors)
    if debug >= 1: print "Error Percentage: "+ str(errorrate)
    if debug >= 1: print "Accuracy: " + str(accuracy)
    if debug >= 2: print "Number of false predictions of a yes vote: " + str(numfalseyes)
    if debug >= 2: print "Number of false predictions of a no vote: " + str(numfalseno)
    stats['Total Errors'] = numerrors
    stats['Accuracy'] = accuracy
    stats['Error Rate'] = errorrate
    stats['Total False Positives'] = numfalseyes
    stats['Total False Negatives'] = numfalseno
    stats['Dataset Size'] = str(dataset_length)
    return stats


def baselineAll( experiment_name='baseline', debug=1, rep_max=None):
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
        stats = baseline(rep_id, debug=debug)
        all_stats[rep_id] = stats

        count += 1

    end = time.time()

    acc = 0
    tot = 0
    for s in all_stats.keys():
        acc += int(all_stats[s]['Total Errors'])
        tot += int(all_stats[s]['Dataset Size'])
    acc = float(acc)/float(tot)

    print
    print  'Total time:   '+str(end-start) + '  seconds.'
    print  'Total Accuracy:   '+str(1-acc)
    print

    return all_stats


def writeResults():
    name = "all__baseline"
    stats= baselineAll()

    print "Done with all reps"
    f = open('experiment_results/'+name+'.json', 'w')
    f.write(json.dumps(stats))
    f.close()

    raw_input("Press Enter to continue... \nAbout to write .csv. Make sure to close the results file if you have it open.")

    # Format stats for excel:
    f = open('experiment_results/'+name+'.csv', 'w')

    #Write headers:
    for stat_name in stats[stats.keys()[0]]:
        f.write(','+stat_name)
    f.write('\n')
    #Write stats
    for rep_id in stats:
        f.write(str(rep_id))
        for stat in stats[rep_id]:
            f.write(','+str(stats[rep_id][stat]))
        f.write('\n')

    f.close()


writeResults()
