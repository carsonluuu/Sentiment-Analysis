#!/bin/bash

# train the models using combined training set
echo '======================================'
echo 'Training the models on combined dataset'
echo '======================================'

python train.py logreg
python train.py svm
python train.py knn

# run them on the combined test set
echo '======================================'
echo 'Running the models on combined test datasets'
echo '======================================'

python test.py ../Data/processed_data/out.csv logreg
python test.py ../Data/processed_data/out.csv svm
python test.py ../Data/processed_data/out.csv knn

echo '======================================'
echo 'Cleaning up...'
echo '======================================'
rm *.pkl