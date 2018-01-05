import numpy

# For the weight vector, each element consists of its key (name of the variable), and the weight)
# For the BOW vector, each element consists of its key (name of the variable), and its count)
BASIC_TYPE = [('value', 'float32'),('key', '|S49')]

WEIGHT_NEGATIVE = -1
WEIGHT_POSITIVE = 1

class MoodBustersReader:
    def __init__(self):
        self.weights = numpy.array([],dtype=[('value', 'float32'),('key', '|S49')])

    # Import a text file with a listing of words to append to the word knowledge base
    # Each word is prescribed an initial weight init_weight
    def import_dictionary(self, dictionary_file, init_weight):
        with open(dictionary_file,"r") as o:
            for line in o.read().splitlines():
                #Skip comments
                if len(line) < 1: continue
                if line[0] == ";": continue
                #Otherwise, add the word to the dictionary with the given weight
                try:
                    self.weights = numpy.append(self.weights,numpy.array([(init_weight,line)], dtype=BASIC_TYPE))
                except UnicodeEncodeError:
                    print("Invalid word found. Skipping")
                    continue

    # Insert an individual word into the dictionary
    def import_word(self,word,init_weight):
        try:
            self.weights = numpy.append(self.weights, numpy.array([(init_weight, word)], dtype=BASIC_TYPE))
        except UnicodeEncodeError:
            print("Unable to encode word into array")

    # Transforms the input text into a feature vector consisting of a bag-of-words vector
    # In the appended information portion of the feature vector, each type of information is represented in one-hot-encoding.
    # For each type of information, the variable for the present category is set to 1, while the other categories are set to 0
    # MAKE SURE THAT THE FINAL DICTIONARY OF WORDS HAS BEEN CREATED (using import_dictionary/import_word) BEFORE CALLING THIS!
    # unfortunately, there is no way
    def create_bow(self, tweet_text):
        # Initialize bow_vector to have zero for all variables
        bow_vector = self.weights.copy()
        for item in bow_vector:
            item['value'] = 0

        # For each word in the text, count the number of times it appears and increase the appropriate variable that it corresponds to by that count
        # For example, "the cat went to the cat", V["the"] = 2, and V["went"] = 1
        for word in tweet_text:
            for item in bow_vector:
                if item['key'].decode('UTF-8') == word:
                    item['value'] += 1

        return bow_vector

    # Given a bag of words vector, if there are more negative than positive words present, return 0. Otherwise, return 1.
    def get_positivity(self, bow_vector):
        positivity = 0.
        for item in bow_vector:
            if item['value'] > 0:
                for w in self.weights:
                    if item['key'] == w['key']:
                        if w['value'] > 0:
                            positivity += item['value']
                        elif w['value'] < 0:
                            positivity -= item['value']
        if positivity >= 0: return 1
        else: return 0