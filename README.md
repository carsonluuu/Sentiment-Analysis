# Sentiment-Analysis
•	Deployed a Twitter crawler using Twitter Streaming API to download tweets and processed these tweets to obtain readable information for fitting model
•	Designed and trained fitting models using logistic regression, SVM and KNN approach
•	Implemented experiment design and evaluation and compared the effectiveness of those approaches
•	Analyzed the data and compared to determine the influence of Thanksgiving holiday on Californian’s moods 

File Stucture:

crawlers:
	|--	clean.sh
	|--	process_json.py
	|--	process_tweet.py
	|--	twitter_streaming.py
	|--	twitter_user.py           // Stores credentials used to get tweets using Twitter's API
	|--	get_training_and_test.py  // Train and test involing
	|--	index.json				  // Emoji ratings JSON file
bag_of_words:
	|--	moodbusters_reader.py
	|--	moodbusters_test.py
	|--	negative-words.txt
	|--	positive-words.txt
	run.sh
	test.py
	train.py