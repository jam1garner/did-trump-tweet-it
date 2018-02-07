import json

print("Opening data...")

with open('master_2016.json','r') as f:
    data = json.loads(f.read())

print("Data retrieved")

newData = []

print("Simplifying data...")
for tweet in data:
    newTweet = {}
    newTweet["id"] = tweet["id"]
    newTweet["text"] = tweet["text"]
    newTweet["exclamations"] = tweet["text"].count('!')
    capsWords = 0
    for i in tweet["text"].split(' '):
        capsWords += int(i.isupper()) and not i == 'I'
    newTweet["caps"] = capsWords
    newTweet["source"] = tweet["source"].replace('<','>').split('>')[2]
    newTweet["mentions"] = len(tweet["entities"]["user_mentions"])
    newTweet["hashtags"] = len(tweet["entities"]["hashtags"])
    newTweet["images"] = 0 if not "media" in tweet["entities"] else len(tweet["entities"]["media"])
    newTweet["notable_names"] = tweet["text"].lower().count('obama') + tweet["text"].lower().count('hillary')
    newTweet["hourOfDay"] = int(tweet["created_at"].split(' ')[3].split(':')[0])
    newTweet["quote"] = int(tweet["text"][0] == '"' or tweet["text"][-1] == '"')
    text = tweet["text"] if tweet["text"][0] != '.' else tweet["text"][1:]
    text.replace('.','!').replace('?','!')
    min_punctuation_distance = 1000
    for i in text.split('!'):
        if len(i) < min_punctuation_distance:
            min_punctuation_distance = len(i)
    text = tweet["text"]
    newTweet["min_punctuation_distance"] = min_punctuation_distance
    newTweet["pauses"] = text.count(",") + text.count("...") + text.count("--")
    newTweet["startsWithPeriod"] = int(text[0] == '.')
    newData.append(newTweet)
print("Data simplified")

print("Writing Data...")
with open("groomed_trump_tweets_2016.json", 'w') as f:
    f.write(json.dumps(newData))
print("Data written.")

#Capitalized words
#Exclamation points
#Hour of day
#Source (iPhone/Android/Web)
#Number of user mentions (entities.user_mentions)
#Number of hash tags (entities.hashtags)
#Number of URLs (entities.urls)
#Mentions of other figures (Obama, Hillary)
#Number of images (entities.media)

#Copy over but don't use:
#Id
#Retweets
#Likes


#hasattr