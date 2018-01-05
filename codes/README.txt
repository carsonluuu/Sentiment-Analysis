Folder Structure:

Code:
	crawlers:
		clean.sh
		process_json.py
		process_tweet.py
		twitter_streaming.py
		twitter_user.py
		get_training_and_test.py
		index.json
	bag_of_words:
		moodbusters_reader.py
		moodbusters_test.py
		negative-words.txt
		positive-words.txt
	run.sh
	test.py
	train.py

crawlers:
	twitter_user.py: Stores credentials used to get tweets using Twitter's API

	twitter_streaming.py: Downloads a configurable number of tweets from twitter with a configurable location setting and outputs the json returned by twitter to a file.

	process_json.py, process_tweet.py: Used to convert the raw json returned by the Twitter API into csv rows with the columns:
	Day of the Week (one-hot), Location (one-hot), Temperature, #retweets, #followers, tweet text

	clean.sh: A shell script that runs process_json.py and process_tweet.py in succession on the data to perform the first pre-processing step.

	get_training_and_test.py: Uses the list of emoji associated with polarity values to indicate associated moods in index.json to look for tweets whose texts contain those emojis. Tweets with text that have a combined positive or negative emoji polarity have their text fields removed and are labelled as happy or sad and added as training data to train.csv. Tweets with no polarity are left with text fields and added to test.csv for further processing as test data.

	index.json: A list of JSON objects matching emoji strongly associated with mood to values between 5 -> -5, with 5 being "most happy" and vice versa.

bag_of_words:
	moodbusters_reader.py: A python class that allows mood prediction of tweets based on words contained in their texts for validation of the effectiveness of the learning models.

	moodbusters_reader.py: Runs moodbusters_reader.py on the test data, removes the text field, and assigns a mood label for approximate validation of learning model effectiveness.

	negative-words.txt: A list of words associated with a negative mood to check for in test data.

	positive-words.txt: A list of words associated with a positive mood.

train.py: A script that can train one of three different models on a training data csv file using sklearn, with the model type (logistic, svm, or knn) and training data path specified in the command line args. The trained models are outputted to corresponding .pkl files.

test.py: A script that uses the specified model file to predict the mood class (happy or sad) of specified test data and outputs performance metrics for model evaluation.

run.sh: A script that trains and tests all models on combined datasets and datasets separated by date of collection and outputs preformance metrics for evaluation of the reproducibility of our project results.