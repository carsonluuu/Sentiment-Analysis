#!/bin/bash
python3 process_json.py
echo 'Done Streaming Data'
python3 process_tweet.py
echo 'Done'