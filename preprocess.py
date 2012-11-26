import extract_features
import hashlib, json, re
from nltk import tokenize
from sets import Set
from pprint import pprint
import string
import config
import operator
from nltk.stem.porter import PorterStemmer

def preprocess(rep_id, bills):
    '''
        Preprocesses all votes/bills for this rep.
        This method only calculates the preprocess data if the md5 of it's inputs or preprocess.py are changed.
        (Either the bills or the preprocessing method is different.)

        Returns:
            A dictionary with all preprocessing data to be passed to the feature generation.
    '''

    loaded = False

    # Load our current cached preprocess data
    try:
        print "Loading preprocess data from store.."
        preprocess_data = json.loads(open('preprocess_data/'+rep_id).read())
        
    except Exception as e:
        preprocess_data = {}


    # If we are using the summary_word_bag
    if 'summary_word_bag' not in config.features_to_ignore: 
        
        # don't regenerate if we loaded it (takes too long)
        if 'summary_word_bag' not in preprocess_data or config.force_preprocess: 
            print ".. Building summary word bag"
            preprocess_data['summary_word_bag'] = generate_summary_word_set(bills)

    # If we are using the bill features
    if 'bill_feature_set' not in config.features_to_ignore:
        print 'Building base feature set for string features'
        preprocess_data['bill_feature_set'] = generate_bill_feature_sets(bills)


    # Write our new preprocess data and hash values
    f = open('preprocess_data/'+rep_id, 'w')
    f.write(json.dumps(preprocess_data))
    f.close()  

    return preprocess_data

st = PorterStemmer()

def generate_summary_word_set(bills):
    ''' Generates a set of frequencies of all words in summaries of bills provided '''
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    word_set = {}


    for bill in bills:
        b = bill['id']
        summary_text = json.loads(open('bill_summaries/'+b).read())
        summary_clean = regex.sub('', summary_text)
        words = tokenize.word_tokenize(summary_clean)

        for w in words:
            if config.stem_words: 
                w = st.stem(w)

            if w in word_set:
                word_set[w] += 1
            else:
                word_set[w] = 1

    word_list = []
    for w in word_set:
        word_list.append((w, word_set[w]))
    word_list = sorted(word_list, key=operator.itemgetter(1), reverse=True)
    pprint(word_list[:100])

    # Apparently we can remove all words only seen once? Interesting I guess. We can comment this in if necessary.
    # TODO(john): Add in NLP additions such as removing word endingds, and possibly bigrams

    return word_set

def generate_bill_feature_sets(bills):
    '''
        Generates the mappings of string features in our bill features to a list of binary features.
        Returns:
            Dictionary as follows: {
                "name of the feature" : {
                        "possible value of feature" : (which bit to turn on)
                    }
            }
            --- Ex: ---
            {
                "lastname": {
                    "Smith": 0,
                    "Baker": 4,
                    "Johnson": 11
                }
            }
    '''
    possible_states = {}

    for bill in bills:
        features = extract_features.extractFeatures(bill)

        # Loop through each feature. If it's a string add it to the possible state list for that feature.
        for f in features:
            if not isinstance(features[f], str): # Only keep track of strings
                continue

            if f not in possible_states:
                possible_states[f] = {}

            # Add the value of this feature to the list of possible values for that feature
            possible_states[f][features[f]] = 0
    
    # Map each feature value to an integer
    for feature in possible_states:
        for i, value in enumerate(possible_states[feature]):
            possible_states[feature][value] = i
            
    return possible_states