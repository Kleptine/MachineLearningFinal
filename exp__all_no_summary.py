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

name = "all_no_summary"

config.features_to_ignore = ['summary_word_bag']
config.force_generate_features = False
config.use_sparse_data = True
config.normalize_data = False
config.normalize_type = 'unit_length' # Other valid option: 'center' (centers/scales distribution around zero)


# Generate our feature vectors
gen_feature_data.genAllExperimentData(experiment_name=name)

# Train the SVM and print results
# TODO(john): Return results in such a way that we can analyze multiple reps
# 	or plug it into excel or something.
stats = svm.svmLearnAll(C=.05, gamma=0.00, kernel='linear', experiment_name=name, debug=1, rep_max=430)


print "Done with all reps"
