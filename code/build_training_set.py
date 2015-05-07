import csv
import time
import google_places
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

X_train = []
Y_train= []
def main():
    generateData()
    regression()

def regression():
    # X_train = sampleArray
    # Y_train = answer
    # Create linear regression object
    regr = linear_model.LinearRegression()
    print "X_train length "+str(len(X_train))
    print "Y_train length "+str(len(Y_train))
    # Train the model using the training sets
    regr.fit(X_train, Y_train)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    print("classifying [[5.0,0,0],[4.5,0,0],[4.9,0,0],[4.6,0,0]]")
    X_test = [[5.0,0,0],[4.5,0,0],[4.9,0,0],[4.6,0,0]]
    print regr.predict(X_test)

def generateData():
    myReader = csv.reader(open('toplist.csv'))
    next(myReader, None) # Skip the header in the csv file
    # for i in range(27):
    #     next(myReader, None) # Skip the header in the csv file
    count = 0
    trainingData = {}
    # sampleArray = []
    # answer = []
    for line in myReader:
        count=count+1
        if count==5:
            time.sleep(1)
            count = 0
        restName = line[0]
        restRanking = float(line[1])
        restLat = float(line[3])
        restLong = float(line[4])
        # print restLat
        # print restLong
        # print restName
        googleDict = google_places.query_google(restLat, restLong, restName)
        location = str(restLat) + "," + str(restLong)
        yelp_info = yelp.query_api(location,search_name=restName)
        print yelp_info

        #infoArray = [rating,sentiment, numReviews]
        if googleDict!=None:
            # print googleDict
            # print "inside"
            # print Y_train
            # print X_train
            infoArray = [googleDict['google_rating'],0,1]
            Y_train.append(restRanking)
            X_train.append(infoArray)
    # return (answer, sampleArray)






if __name__ == '__main__':
    main()
