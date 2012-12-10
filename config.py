'''
	Stores global data between modules. This can be modified, so don't assume they're constants. 
'''

# Valid features to ignore: 
# 'bill_feature_set'
# 'summary_word_bag'
# Any key of a feature extracted in extract_features.
# -----
# Summary disabled by default
features_to_ignore = ['summary_word_bag']

#0 for svm 
#1 for decision tree 
classifier= 0 
 
#whether we should use validation set
validate= False
# Do we want to ignore abstaining votes
remove_abstaining_votes = True      

# Ignore caching for our feature vectors. Might take a little while to generate.
force_generate_features = False

# Ignore caching for preprocessing when generating feature vectors. Takes a while when using summary bag.
force_preprocess = False

# Whether to convert feature vectors into sparse arrays
use_sparse_data = False


#Whether to normalize our data
normalize_data = False

# How to normalize the data
#  unit_length: Scales individual vectors to have a unit length
#  center: Centers and scales data to fit around zero.
normalize_type = 'unit_length'


# Whether to stem words for the summaries 
stem_words = False

# --------------------------- globals
scaler = None

