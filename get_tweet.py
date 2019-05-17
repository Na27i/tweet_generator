import json
import sys
import pandas

args = sys.argv

if len(args) == 1 :
    import main as settings
else :
    import sub as settings

from requests_oauthlib import OAuth1Session

CK = settings.CONSUMER_KEY
CS = settings.CONSUMER_SECRET
AT = settings.ACCESS_TOKEN
ATS = settings.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

tweetlist = []

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

params = {"count" : 200}

res = twitter.get(url, params = params)
if res.status_code == 200:
    timelines = json.loads(res.text)
    for tweet in timelines:
        tweetlist.append(tweet["text"])
else:
    print("取得失敗(%d)" % res.status_code)

datafile = pandas.DataFrame(tweetlist)
datafile.to_csv("tweetlist.csv", encoding='utf_8_sig')