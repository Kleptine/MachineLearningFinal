import gen_feature_data
import svm
import config
from gen_feature_data import load_json
import json


'''
Generic experiment with no summary features.
Runs on all representatives, and saves results under experiment_results/all_no_summary
Note: only runs on 20 for now
'''

name = "all_no_summary_validation"

config.features_to_ignore = ['summary_word_bag']
config.force_generate_features = False
config.use_sparse_data = True
config.normalize_data = False
config.normalize_type = 'unit_length' # Other valid option: 'center' (centers/scales distribution around zero)
config.validate= True


# Generate our feature vectors 
gen_feature_data.genAllExperimentData(experiment_name=name) #********************************************************************** seeeeeee)


#Train the SVM and print results

#try the C values in Cs for each kernel in kernels
kernels= ['linear']
Cs= [0.001,0.01,0.003]
stats = svm.svmLearnAll(C=.01, gamma=0.00, kernel='linear', experiment_name=name, debug=1, rep_max=None,Clist=Cs,kernelList=kernels,mcnemar=True)

mcnemardata={}

for (rep_id,repstats) in stats.items():
    if ('WrongPredictions') in repstats.keys():
        bills=repstats['WrongPredictions']
        mcnemardata[rep_id]=bills
        del(repstats['WrongPredictions'])

mcn= open("mcnemar_data/"+name,'w')
mcn.write(json.dumps(mcnemardata))
mcn.close()


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
