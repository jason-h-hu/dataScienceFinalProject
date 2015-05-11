import util
import csv
import time
import google_places
# import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import yelp
import ranking
import json
from sklearn import datasets
from sklearn import linear_model
import matplotlib.pyplot as plt
from sklearn import cross_validation
from sklearn import metrics
import random
from sklearn import linear_model
from sklearn import preprocessing



def main():
    regression()



def regression():
    # Create linear regression object
    with open('trainingData.json') as f:
        jsonData = json.load(f)
    X_train = jsonData['X_train']
    Y_train = jsonData['Y_train']
    Y_train = np.array(Y_train)
    X_train = np.array(X_train)
    X_train = preprocessing.scale(X_train)
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)

    # The coefficients
    print('Coefficients: \n', regr.coef_)

    # The mean square error
    print("Residual sum of squares: %.2f"
          % np.mean((regr.predict(X_train) - Y_train) ** 2))
    print ("score of regression is"+str(regr.score(X_train, Y_train)))
    meanDiffs = []
    
    print X_train.shape
    for i in range(10):
        randomNum = random.randrange(1,10)
        X_CV_train, X_CV_test, y_CV_train, y_CV_test = cross_validation.train_test_split(X_train, Y_train, test_size=0.1, random_state=0)
        CVregr = linear_model.LinearRegression().fit(X_CV_train, y_CV_train)
        meanDiffs.append(np.mean((CVregr.predict(X_CV_test) - y_CV_test) ** 2))
    cvSquaredError = np.mean(meanDiffs)
    print ("cv mean squared error is" + str(cvSquaredError))
    
    return regr





if __name__ == '__main__':
    main()
