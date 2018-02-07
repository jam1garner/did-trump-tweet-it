# Did Trump Tweet it?

A KNN looking at a number of factors to determine if Trump was the one who sent the tweet.

Paramaters used:
* Hour of day
* Whether or not it had a picture/link
* Whether or not the tweet was in quotes
* Exclamation points!
* ALL CAPS WORDS
* @mentions
* #hashtags
* Notable names (Hillary, Obama)
* Minimum punctuation distance (Usually equates to sentence length in characters, some are very big others are not. SMALL!)
* Number of “pauses” this includes… ellipses, commas — even dashes

Requirements:
* Scikitlearn
* numpy
* scipy
* Python 3

Technical write up: https://medium.com/@jam1garner/did-trump-tweet-it-15c33e5e6b07
