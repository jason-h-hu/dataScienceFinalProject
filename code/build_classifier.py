import csv
import time
import google_places
# import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import yelp
import ranking
import json



def main():
    regression()



def regression():
    # Create linear regression object
    with open('trainingData.json') as f:
        jsonData = json.load(f)
    X_train = jsonData['X_train']
    Y_train = jsonData['Y_train']
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    print(" X_test = [[5.0,0,1000],[5.0,1000,1000],[4.5,0,450], [4.5,-50,450],[4.9,0,455],[4.6,0,2],[4.6,2.1,2],[4.6,2.1,2],[1,0,5000],[1,25,5000],[1.1,0,5],[2,0,300]]")
    X_test = [[5.0,0,1000],[5.0,1000,1000],[4.5,0,450], [4.5,-50,450],[4.9,0,455],[4.6,0,2],[4.6,2.1,2],[4.6,2.1,2],[1,0,5000],[1,25,5000],[1.1,0,5],[2,0,300]]
    print regr.predict(X_test)
    return regr





if __name__ == '__main__':
    main()
