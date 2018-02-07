import json
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API

#Variables that contains the user credentials to access Twitter API 
access_token = "707372780463853569-2ejgsIfd5CGQLJiSneTtDaJiNE2dcJ6"
access_token_secret = "99jVP3Q9LkIQ0VqlPXUAewGNBonuzz53ObFQ86NPtiHUC"
consumer_key = "OkrSqnS3FKwh3gkH6TOuhoatL"
consumer_secret = "vJOmcO5fL3dfEziNMTrfdPhjzDiy4MVsk5D9YQJSbECC6m4BAn"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    api = API(auth_handler=auth)
    status = api.get_status(948355557022420992)
    print(status)

tweet = status._json
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
print(newTweet)