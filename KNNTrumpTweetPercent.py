import json
from sklearn.neighbors import KNeighborsClassifier

def loadDataset(trainingSet=[], trainingClass=[], testSet=[], testClass=[], testTweetIds=[]):
    with open("groomed_trump_tweets_2016.json", "r") as f:
        data = json.loads(f.read())

    tweetIds = []
    dataSet = []
    dataClass = []
    for tweet in data:
        tweetIds.append(tweet["id"])
        isAndroid = 1 if tweet["source"] == "Twitter for Android" else 0
        dataSet.append([tweet["exclamations"],
                        tweet["caps"],
                        tweet["mentions"],
                        tweet["hashtags"],
                        tweet["images"],
                        tweet["notable_names"],
                        tweet["hourOfDay"],
                        tweet["quote"],
                        tweet["min_punctuation_distance"],
                        tweet["pauses"]])
        dataClass.append(isAndroid)


    maxVals = [0] * (len(dataSet[0]) - 1)
    minVals = [0xFFFFFFFF] * (len(dataSet[0]) - 1)
    for i in range(len(maxVals)):
        for tweet in dataSet:
            if minVals[i] > tweet[i]:
                minVals[i] = tweet[i]
            if maxVals[i] < tweet[i]:
                maxVals[i] = tweet[i]

    weights = [1, 1, 1, 1, 1, 1, 1, 1000000, 1, 1]
    for i in range(len(maxVals)):
        valRange = maxVals[i] - minVals[i]
        for tweet in dataSet:
            tweet[i] -= float(minVals[i])
            tweet[i] /= valRange
            tweet[i] *= weights[i]

    trainingSet += dataSet[::2]
    trainingClass += dataClass[::2]
    testSet += dataSet[1::2]
    testClass += dataClass[1::2]
    testTweetIds += tweetIds[1::2]
    return trainingSet, trainingClass, testSet, testClass, testTweetIds

def train(trainingSet, trainingClass):
    model = KNeighborsClassifier(n_neighbors=10)
    model.fit(trainingSet, trainingClass)
    return model

# Modes for printTweetIds - None, 'all', 'wrong', 'correct'
def test(model, testSet, testClass, testTweetIds=[], printTweetIds=None):
    correct = 0
    wrong = 0
    answers = model.predict(testSet)
    probabilities = model.predict_proba(testSet)
    for i in range(len(testSet)):
        answer = answers[i]
        probability = probabilities[i]
        if answer == testClass[i]:
            correct += 1
            if printTweetIds in ['all', 'correct']:
                print("https://twitter.com/realDonaldTrump/status/%i | Probability - %f | Correct" % (testTweetIds[i], probability[answer]))
        else:
            wrong += 1
            if printTweetIds in ['all', 'wrong']:
                if testClass[i] == 0:
                    print("https://twitter.com/realDonaldTrump/status/%i | Probability - %f | Wrong" % (testTweetIds[i], probability[answer]))
    percentCorrect = (correct / (correct + wrong)) * 100
    print(percentCorrect)

def main():
    trainingSet, trainingClass, testSet, testClass, testTweetIds = loadDataset()
    model = train(trainingSet, trainingClass)
    test(model, testSet, testClass, testTweetIds, 'wrong')

if __name__ == "__main__":
    main()
