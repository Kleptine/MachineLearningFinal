import gen_feature_data
import svm
import config
from gen_feature_data import load_json

'''
Generic experiment with no summary features.
'''
    
name = "summary"
rep_id = '400404'
rep_data = load_json('representatives')[rep_id]

config.features_to_ignore = []
config.force_preprocess = True
config.use_sparse_data = True


print
print '====================================='
print '       '+name
print '====================================='
print 


# Generate our feature vectors
# TODO(john): Cache this before we start to massive tests to save time
gen_feature_data.genExperimentData(rep_id, experiment_name=name)

# Train the SVM and print results
# TODO(john): Return results in such a way that we can analyze multiple reps
# 	or plug it into excel or something.
svm.svmLearn(rep_id, C=1, gamma=1.0, kernel='rbf', debug=1, experiment_name=name)
