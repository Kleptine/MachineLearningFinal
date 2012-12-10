import gen_feature_data
import svm
import config
from gen_feature_data import load_json
import json
import dateutil.parser as dateparse
import httplib

'''
Generic experiment with no summary features.
Runs on all representatives, and saves results under experiment_results/all_no_summary
'''

name = "all_bill_predict"

config.features_to_ignore = ['summary_word_bag']
config.force_generate_features = False
config.use_sparse_data = True
config.normalize_data = False
config.normalize_type = 'unit_length' # Other valid option: 'center' (centers/scales distribution around zero)

# Load the saved SVM's from the following experiment. (They're saved now when you run svm.svmLearn)
rep_svms = svm.loadSVMs('all_no_summaries')

# Test each SVM on the each bill
#for b in features

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