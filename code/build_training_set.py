import csv
import time
import google_places
# import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import yelp
import ranking
import sentiment_builder

X_train = []
Y_train= []
def main():
    restList = generateRestInfo()
    getRestData(restList)
    regression()

def getRestData(restList):
    # print restList
    restList = ranking.create_weighted_stars(restList)
    restList =sentiment_builder.build_sent_entry(rests)
    for rest in restList:
        weightedStars= rest['weighted_stars']
        sentiment = rest['sentiment']
        numReviews = rest['num_yelp_reviews']
        featureArray = [weightedStars, sentiment, numReviews]
        Y_train.append(rest['ranking'])
        X_train.append(featureArray)
    # infoArray = [rating,0,yelp_info['num_yelp_reviews']]
                # Y_train.append(restRanking)
                # X_train.append(infoArray)
    # print restList


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
    print(" X_test = [[5.0,0,1000],[5.0,1000,1000],[4.5,0,450], [4.5,-50,450],[4.9,0,455],[4.6,0,2],[4.6,2.1,2],[4.6,2.1,2],[1,0,5000],[1,25,5000],[1.1,0,5],[2,0,300]]")
    X_test = [[5.0,0,1000],[5.0,1000,1000],[4.5,0,450], [4.5,-50,450],[4.9,0,455],[4.6,0,2],[4.6,2.1,2],[4.6,2.1,2],[1,0,5000],[1,25,5000],[1.1,0,5],[2,0,300]]
    print regr.predict(X_test)

def generateRestInfo():
    myReader = csv.reader(open('toplist.csv'))
    next(myReader, None) # Skip the header in the csv file
    # for i in range(27):
    #     next(myReader, None) # Skip the header in the csv file
    count = 0
    trainingData = {}
    restList = []
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
        # print restName
        # yelp_info = yelp.query_api(location,search_name=restName)
        # print yelp_info

        #infoArray = [rating,sentiment, numReviews]
        if googleDict!=None:
            # print googleDict
            # print "inside"
            # print Y_train
            # print X_train
            yelp_info = yelp.query_api(location,search_name=restName)
            # print yelp_info
            if yelp_info!=None:
                restDict = {}
                restDict['ranking']=restRanking
                restDict['google_rating']=googleDict['google_rating']
                restDict["google_review_list"]=googleDict['reviews']
                restDict["google_rating"]=googleDict['google_rating']
                restDict["num_yelp_reviews"] = yelp_info['num_yelp_reviews']
                restDict['yelp_star']=yelp_info['yelp_star']
                restDict['yelp_review']=yelp_info['yelp_review']
                # restDict['training_rating'] = np.average([restDict['yelp_star'], restDict['google_rating']])
                # weightedRating = ranking.rate
                restList.append(restDict)


                # infoArray = [rating,0,yelp_info['num_yelp_reviews']]
                # Y_train.append(restRanking)
                # X_train.append(infoArray)
    # return (answer, sampleArray)
    return restList





if __name__ == '__main__':
    main()
