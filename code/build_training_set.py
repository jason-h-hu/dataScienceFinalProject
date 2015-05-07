import csv
import time
import google_places


def main():
    myReader = csv.reader(open('toplist.csv'))
    next(myReader, None) # Skip the header in the csv file
    count = 0
    trainingData = {}
    for line in myReader:
        count=count+1
        if count==5:
            time.sleep(1)
            count = 0
        restName = line[0]
        restRanking = float(line[1])
        restLat = float(line[3])
        restLong = float(line[4])
        print restLat
        print restLong
        print restName
        googleDict = google_places.trainingQueryGoogle(restLat, restLong, restName)
        print googleDict
        #infoArray = [rating,sentiment, numReviews]
        # infoArray = [googleDict['google_rating'],0,1]
    #     answer.append(restRanking)
    #     sampleArray.append(infoArray)
    # print answer
    # print sampleArray






if __name__ == '__main__':
    main()
