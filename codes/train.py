import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.cross_validation import cross_val_score
from sklearn.externals import joblib

# Training Data with labels assigned based on emojis found in texts
# Test Data has labels assigned based on whether there are more positive or negative words in texts

# Reads the data from CSV files, converts it into Dataframe and returns x and y dataframes
def getDataframe(filePath):
    y = pd.read_csv(filePath, header=None, usecols=[13], squeeze=True)
    x = pd.read_csv(filePath, header=None, usecols=[i for i in range(13)])
    return x, y

def main():
	pathname = "../Data/processed_data/train.csv"
	if (sys.argv[1] == 'knn'):
		# instantiate a kNN model
		k = 5
		knn = KNeighborsClassifier(n_neighbors=k)

		# get the data
		train_x, train_y = getDataframe(pathname)
		train_x = preprocessing.scale(train_x)

		# fit with X and y
		print("Fitting under kNN model...")
		knn = knn.fit(train_x, train_y)
		print("Training data accuracy:", knn.score(train_x, train_y))

		# 5-fold cross validation... determine accuracy
		cv_scores = cross_val_score(KNeighborsClassifier(n_neighbors=k), train_x, train_y, scoring='accuracy', cv=5)
		print("5-fold cross validation:", cv_scores.mean())

		# dumps out the saved linearRegression model
		joblib.dump(knn, 'knn.pkl')
	elif (sys.argv[1] == 'logreg'):
		# instantiate a logistic regression model
		logreg = LogisticRegression()

		# get the data
		train_x, train_y = getDataframe(pathname)

		# fit with X and y
		print("Fitting under logistic regression model...")
		logreg = logreg.fit(train_x, train_y)
		print("Training data accuracy:", logreg.score(train_x, train_y))

		# 5-fold cross validation... determine accuracy
		cv_scores = cross_val_score(LogisticRegression(), train_x, train_y, scoring='accuracy', cv=5)
		print("5-fold cross validation:", cv_scores.mean())

		# dumps out the saved linearRegression model
		joblib.dump(logreg, 'logreg.pkl')
	elif (sys.argv[1] == 'svm'):
		# instantiate a SVM model
		support_vector = svm.SVC()

		# get the data
		train_x, train_y = getDataframe(pathname)
		train_x = preprocessing.scale(train_x)

		# fit with X and y
		print("Fitting under SVM model...")
		support_vector = support_vector.fit(train_x, train_y)
		print("Training data accuracy:", support_vector.score(train_x, train_y))

		# 5-fold cross validation... determine accuracy
		cv_scores = cross_val_score(svm.SVC(), train_x, train_y, scoring='accuracy', cv=5)
		print("5-fold cross validation:", cv_scores.mean())

		# dumps out the saved linearRegression model
		joblib.dump(support_vector, 'svm.pkl')
	else:
		print("Bad name!")


if __name__ == "__main__":
    main()
