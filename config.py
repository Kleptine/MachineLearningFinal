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


# Do we want to ignore abstaining votes
remove_abstaining_votes = True      