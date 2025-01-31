# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 15:15:59 2016

@author: roosv_000

Ensemble of 5 models. Label probalilities/binary labels for the test businesses predicted by five different models are imported. 
By setting weights for each model one submission file is made.
MODELS:
- Statistical model, the probability of a label occurring for a business.
- SVM mean model, takes the mean caffe-features per business, and uses an SVM to classify.
- Color Feature model, takes mean Color feature per business, and uses Random Forest to classify.
- Per Photo SVM model, predict labels per photo with SVM of caffe features than another SVM to predict per business.
- Cluster model 

set:
-model directories
-SubmissionFormat file directory
-weights
-filename for submission file
"""

import numpy as np
import pandas as pd

#load models, every model consist of a matrix label probabilities for all businesses in the test set.
model1 = pd.read_csv('probSTAT.csv', sep=';', header=None).values
model2 = pd.read_csv('probSVM.csv',sep=',', header=None).values
model3 = pd.read_csv('probColor.csv',sep=',', header=None).values
model4 = np.load('../Labels per photo/data_array_test_9-4.onallprob.npy')
model5= np.load('../Labels per photo/Test_Clusters_12-4.OnAll_Linear.npy')

#import the example submission file for its stucture
submit = pd.read_csv('SubmissionFormat.csv',sep=',')

#weights for the models, if you only want to ensemble 2 methods set the third and forth value on 0
weights =  [0.05, 0.75, 0, 0.15, 0.05]

## Use this if you want to specify varying weights per label per model.
#Weightmatrix1 = np.array([[0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 ],]*10000)
#Weightmatrix2 = np.array([[0.7  , 0.7  , 0.7  , 0.7  , 0.7  , 0.7  , 0.7  , 0.7  , 0.7  ],]*10000)
#Weightmatrix3 = np.array([[0    , 0    , 0    , 0    , 0    , 0    , 0    , 0    , 0    ],]*10000)
#Weightmatrix4 = np.array([[0.2  , 0.2  , 0.2  , 0.2  , 0.2  , 0.2  , 0.2  , 0.2  , 0.2  ],]*10000)
#Weightmatrix5 = np.array([[0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 , 0.05 ],]*10000)

# Set a filename for the submission file
filename = 'Ensembletest_5_Models_meanSVM_perphotolin_05_70_20_nonlin_05lin.csv'

#classification threshold
threshold = 0.5

#Create one matrix with the probability for each label for every business, by combining the probabilities in the models with certain weights.
#ensembleprob = model1 * Weightmatrix1 + model2 * Weightmatrix2 + model3 * Weightmatrix3 + model4 * Weightmatrix4 +model5 * Weightmatrix5
ensembleprob = model1 * weights[0] + model2 * weights[1] + model3 * weights[2] + model4 * weights[3] +model5 * weights[4]

#Classify by converting probabilities into binaries with help of the threshold.
ensembleprob[ensembleprob > threshold] = 1
ensembleprob[ensembleprob <= threshold] = 0

#convert array ensembleprob [0 1 0 0 0 1] to list of strings ['2 6']
predList = []
for row in ensembleprob:
        indices = [str(index) for index,number in enumerate(row) if number == 1.0]
        sep = " "
        labelstr = sep.join(indices)
        predList.append(labelstr)

# Put labels(predList) in de submissionfile colomn named 'labels'
submit['labels' ] = predList

#save in csv file
submit.to_csv(filename,index=False)