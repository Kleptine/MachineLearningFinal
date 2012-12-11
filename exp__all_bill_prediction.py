import gen_feature_data
import svm
import config
from gen_feature_data import load_json
import json
import dateutil.parser as dateparse
import httplib
import preprocess
import extract_features
import gen_feature_data
import numpy as np

'''
Generic experiment with no summary features.
Runs on all representatives, and saves results under experiment_results/all_no_summary
'''

name = "all_bill_predict"

config.features_to_ignore = ['summary_word_bag']
config.force_generate_features = True
#config.force_preprocess = True
config.use_sparse_data = True
config.normalize_data = False
config.normalize_type = 'unit_length' # Other valid option: 'center' (centers/scales distribution around zero)


# Load in all bills and votes
reps = json.loads(open('representatives').read())
bills = json.loads(open('bill_prediction/bills').read())
votes_s = json.loads(open('bill_prediction/votes').read())['objects']
votes = []
print 'Done loading votes'

for v in votes_s:
  if v['chamber'] != 'senate':
    votes.append(v)

results = {}

for rep_id in reps:
  print  '---------------------  ', rep_id
  # Generate preprocess on train bills!
  gen_feature_data.getData(rep_id, 'rep_votes_train', preprocess_data=None)
  pre_data = json.loads(open('preprocess_data/'+rep_id).read())
  model = svm.loadSVM('all_no_summary', rep_id)
  print 'Loaded model and data.'
  #print votes_
  for i, v in enumerate(votes):
    vector, _ = extract_features.generate_feature_vector(bills[i], pre_data)
    test_data = np.array(vector)

    prediction = model.predict(test_data)
    print prediction

    if v['id'] not in results:
      results[v['id']] = 0
    results[v['id']] += prediction

    
    
for v in votes:
  nums = v['required'].split('/')
  req_percentage = float(nums[0]) / float(nums[1])   

  percentage = float(results[v['id']]) / len(reps)

  print
  print "=================================="
  print "Got:       ", percentage
  print "Required:  ", req_percentage

exit()

# Test each SVM on the each bill
for s in rep_svms:
  svm.predict_single(bill)


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