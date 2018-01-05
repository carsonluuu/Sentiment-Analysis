import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn import metrics
from sklearn import preprocessing
from sklearn.externals import joblib

# sample command: python3 test.py test.csv logreg

# Reads the data from CSV files, converts it into Dataframe and returns x and y dataframes
def getDataframe(filePath):
    y = pd.read_csv(filePath, header=None, usecols=[13], squeeze=True)
    x = pd.read_csv(filePath, header=None, usecols=[i for i in range(13)])
    return x, y

def main():
	test_x, test_y = getDataframe(sys.argv[1]) # 'test.csv'
	test_x = preprocessing.scale(test_x)
	model = -1
	
	name = sys.argv[2]
	if (name == 'svm'):
		model = joblib.load('svm.pkl') 
	elif (name == 'knn'):
		model = joblib.load('knn.pkl')
	elif (name == 'logreg'):
		model = joblib.load('logreg.pkl')
	else:
		print("Invalid Name")
		return

	# make prediction...
	print("===" + name + "===")
	predicted = model.predict(test_x)

	# calculate positive-negative ratio
	num_zero, num_one = 0, 0
	for i in predicted:
		if i == 0:
			num_zero += 1
		else:
			num_one += 1

	num_zero_act, num_one_act = 0, 0
	for i in test_y:
		if i == 0:
			num_zero_act += 1
		else:
			num_one_act += 1
	pn_ratio = 1 if num_zero == 0 else float(num_one) / num_zero
	print("The positive-negative ratio predicted is", pn_ratio)
	pn_ratio_act = 1 if num_zero_act == 0 else float(num_one_act) / num_zero_act
	print("The actual positive-negative ratio predicted is", pn_ratio_act)

	# some evaluation metrics
	print("Test data accuracy:", metrics.accuracy_score(test_y, predicted))
	print("Showing classification report...")
	print(metrics.classification_report(test_y, predicted))

if __name__ == "__main__":
    main()