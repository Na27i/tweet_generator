import json
import random

from janome.tokenizer import Tokenizer
from requests_oauthlib import OAuth1Session

import main as settings

CK = settings.CONSUMER_KEY
CS = settings.CONSUMER_SECRET
AT = settings.ACCESS_TOKEN
ATS = settings.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)


#文章＝連用句＋体言句＋用言句
do = []     #動詞
keiyo = []  #形容詞
keido = []  #形容動詞
mei = []    #名詞
huku = []   #副詞
rentai = [] #連体詞
setu = []   #接続詞
kando = []  #感動詞
zyodo = []  #助動詞
zyo = []    #助詞

tweet = ""
tweetlist = ""
sent = ""

post_url = "https://api.twitter.com/1.1/statuses/update.json"
get_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
get_params = {"count" : 200, "exclude_replies":True, "include_rts":False}
get_res = twitter.get(get_url, params = get_params)

if get_res.status_code == 200:
    timelines = json.loads(get_res.text)
    #全ツイートを取得
    for i in timelines:
        tweet = (i["text"])
        tweet = tweet.split("http" , 1)[0]   #urlを削除
        tweet = tweet.split("@", 1)[0]  #usernameを削除
        tweet = tweet.split(" ")[0]   #半角スペースを削除
        tweet = tweet.split("　")[0]   #全角スペースを削除
        tweetlist += tweet

    #助詞()
    t = Tokenizer()
    tokens = t.tokenize(tweetlist)
    for token in tokens:
        partOfSpeech = token.part_of_speech.split(',')[0]
        if partOfSpeech == u"動詞":
            do.append(token.surface)
        elif partOfSpeech == u"形容詞":
            keiyo.append(token.surface)
        elif partOfSpeech == u"形容動詞":
            keido.append(token.surface)
        elif partOfSpeech == u"名詞":
            mei.append(token.surface)
        elif partOfSpeech == u"副詞":
            huku.append(token.surface)
        elif partOfSpeech == u"連体詞":
            rentai.append(token.surface)
        elif partOfSpeech == u"接続詞":
            setu.append(token.surface)
        elif partOfSpeech == u"感動詞":
            kando.append(token.surface)
        elif partOfSpeech == u"助動詞":
            zyodo.append(token.surface)
        elif partOfSpeech == u"助詞":
            zyo.append(token.surface)

    #連用句の追加
    #ren = random.randrange(2)
    #if ren == 0:
    sent += huku[random.randrange(len(huku))]


    #体言句の追加
    if len(zyo) == 0:
        tai = mei[random.randrange(len(mei))]
    else :
        tai = mei[random.randrange(len(mei))] + zyo[random.randrange(len(zyo))]
    sent += tai


    #用言句の追加
    you = random.randrange(3)
    if you == 2:
        if len(keido) != 0:
            sent += keido[random.randrange(len(keido))]
        else :
            you -= 1
    if you == 1:
        if len(keiyo) != 0:
            sent += keiyo[random.randrange(len(keiyo))]
        else :
            you -= 1
    else:
        if len(keiyo) != 0:
            sent += do[random.randrange(len(do))]

    sent += "  (みがわりったー)"
    print(sent)

    post_params = {"status" : sent}
    post_res = twitter.post(post_url, params = post_params)
else:
    print("取得失敗(%d)" % get_res.status_code)
