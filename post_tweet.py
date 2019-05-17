import json
import sys

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

url = "https://api.twitter.com/1.1/statuses/update.json"

tweet = ''

print("Please input new tweet.")
while 1:
    sent = input('>> ')
    if sent == "quit":
        break
    else:
        tweet += sent
        tweet += '\n'

params = {"status" : tweet}

res = twitter.post(url, params = params)

if res.status_code == 200:
    print("投稿成功")
else:
    print("投稿失敗")