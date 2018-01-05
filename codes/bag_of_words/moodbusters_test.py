import moodbusters_reader as mb
import csv
bowmaker = mb.MoodBustersReader()
bowmaker.import_dictionary('positive-words.txt',mb.WEIGHT_POSITIVE)
bowmaker.import_dictionary('negative-words.txt',mb.WEIGHT_NEGATIVE)
f1 = open("test.csv","r") # open input file for reading
with open('out.csv', 'w') as f: # output csv file
    writer = csv.writer(f)
    with f1 as csvfile: # input csv file
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
        	text = bowmaker.create_bow(row[13].split())
        	row[13] = bowmaker.get_positivity(text)
        	writer.writerow(row)
f1.close()   