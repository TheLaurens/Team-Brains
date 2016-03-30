'''
Trains a random forest to the data with features per business.
Gives a classification for the test data.
'''

from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from CreateClassification import create
from LoadData import load, load_features
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import matplotlib.pyplot as plt

'''trains a random forest on the given train data. Returns the forest.'''
def trainForest(Xtrain, Ytrain):
    '''RANDOM FOREST'''
    forest = RandomForestClassifier()
    forest.fit(Xtrain,Ytrain)
    return forest

'''applies 10 fold cross validation on the given forest for the given traindata. Returns the scores.'''
def validateForest(forest, Xtrain, Ytrain):
    #accuracy on train set, 10 fold cross validation
    scores = cross_validation.cross_val_score(forest, Xtrain, Ytrain, cv=10, scoring='f1_weighted')
    print("Accuracy RF: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
    return scores

'''Predicts the classes for the test data and saves it in a csv file. Returns true if csv file is created.'''
def createClassification(forest,Xtest, XtestDF):
    '''CREATE CLASSIFICATION'''
    Ypred = forest.predict(Xtest)
    return create(Ypred, XtestDF)

'''Loads the data and turns it into arrays of the correct shape. Returns the data in a dictionary.'''
def getData():
    # Load train data: X
    featureData = load_features('input')
    Xtrain = featureData['TRAIN_F']
    Xcols = Xtrain.columns.tolist() #business_id, r_mean, r_sd, g_mean, g_sd, b_mean, b_sd, imagecount, h_mean, h_sd, w_mean, w_sd

    # Load train data: Y
    data = load('input')
    Ytrain = data['Y_TRAIN']
    Ycols = Ytrain.columns.tolist() #business_id, 0, 1, 2, 3, 4, 5, 6, 7, 8

    '''CREATE ARRAYS'''

    #merge X and Y. Reasons: order should be the same. Labels could contain businesses that are removed during preprocessing.
    trainData = pd.merge(Xtrain, Ytrain, on='business_id')

    #split Xtrain and Y train into two arrays, without business_id!
    del Xcols[0] #remove business_id from list
    del Ycols[0] #remove business_id from list
    Xtrain = trainData[Xcols].values
    Ytrain = trainData[Ycols].values

    #create array from test data
    XtestDF = featureData['TEST_F']
    Xtest = XtestDF[Xcols].values

    data = {
        'Xtrain' : Xtrain,
        'Ytrain' : Ytrain,
        'Xtest' : Xtest,
        'XtestDF' : XtestDF,
    }
    return data


''' Source: http://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html'''
def showFeatureImportance(forest,Xtrain):
    # Build a forest and compute the feature importances
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(Xtrain.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(Xtrain.shape[1]), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(Xtrain.shape[1]), indices)
    plt.xlim([-1, Xtrain.shape[1]])
    plt.show()