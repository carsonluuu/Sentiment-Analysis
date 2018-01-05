import json
import os
import unicodecsv as csv
from uniseg import graphemecluster as gc

## Get the emoji-polarity dictionary from the json file.
emoji_dict = {}
with open('index.json') as emoji_file:
    emoji_data = json.load(emoji_file)
    for json_obj in emoji_data:
        emoji_dict[json_obj['emoji']] = json_obj['polarity']

def extract_emojis(str):
  return list(gc.grapheme_clusters(str))

def process_csv_row(row):
    dow_onehot = row[0]
    location_onehot = row[1]
    temperature = row[2]
    retweets = row[3]
    followers = row[4]
    text = row[5]
    new_row = []

    for char in dow_onehot:
        if char == '0':
            new_row.append(0)
        elif char == '1':
            new_row.append(1)
    for char in location_onehot:
        if char == '0':
            new_row.append(0)
        elif char == '1':
            new_row.append(1)

    new_row.append(temperature)
    new_row.append(retweets)
    new_row.append(followers)

    text_emojis = extract_emojis(text)
    polarity = 0
    for text_emoji in text_emojis:
        if text_emoji in emoji_dict.keys():
            polarity += emoji_dict[text_emoji]

    if polarity > 0:
        new_row.append(1)
        return (True, new_row)
    elif polarity < 0:
        new_row.append(0)
        return (True, new_row)
    else:
        new_row.append(text)
        return (False, new_row)

## Look through all result.csv files, label data points where the text
## gives a meaningful emoji polarity value, and use the rest as test data.
root_dir = './data'
for dir_name, subdir_list, file_list in os.walk(root_dir):
    print 'Found directory: ' + dir_name
    for file_name in file_list:
        if file_name == 'result.csv':
            with open(dir_name + '/' +  file_name, 'r') as result_file, open(dir_name + '/train.csv', 'w') as training_file, open(dir_name + '/test.csv', 'w') as test_file:
                result_reader = csv.reader(result_file, encoding='utf-8')
                training_writer = csv.writer(training_file, encoding='utf-8')
                test_writer = csv.writer(test_file, encoding='utf-8')
                for row in result_reader:
                    row_tuple = process_csv_row(row)
                    if row_tuple[0]:
                        training_writer.writerows([row_tuple[1]])
                    else:
                        test_writer.writerows([row_tuple[1]])
