from flask import Flask, jsonify
from flask import request
import tweepy
from tweepy import Stream
#from pymongo import Connection
from tweepy import Stream
from flask import Response
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import json
from bson import Binary, Code
from bson.json_util import dumps
import pymongo

class DBhandler:
    def __init__(self):
        try:
            self.client=MongoClient()
            #return True
        except Exception,e:
            pass
            #return False

    def createConnection(self,username,password,port):
        try:
            self.client=MongoClient('mongodb://%s:%s@127.0.0.1:%s' % (username, password,port))
            return True
        except Exception,e:
            return False

    def closeConnection(self):
        try:
            self.client.close()
            return [True]
        except Exception,e:
            return [False,e]

    def insert(self,database,collection,jsondata):
        try:
            db=self.client[database]
            #print(type(jsondata._json))
            res=db[collection].insert_one(json.loads(jsondata))
            #print(jsondata)
            return [True,res]
        except Exception,e:
            print(e)
            return [False,e]



    def getdata(self,database,collection):
        try:
            db=self.client[database]
            res=db[collection].find()
            return [True,json.loads(dumps(res))]
        except Exception,e:
            return [False,e]

    def getSortedData(self,database,collection,key,reverse):
        try:
            db=self.client[database]
            if reverse:
                res=db[collection].find().sort(key,pymongo.DESCENDING)
            else:
                res=db[collection].find().sort(key,pymongo.ASCENDING)
            return [True,json.loads(dumps(res))]
        except Exception,e:
            return [False,e]

    def getrangeFilter(self,database,collection,key,begin,end):
        try:
            db=self.client[database]
            res=db[collection].find({key:{'$gte':begin,'$lte':end}})
            return [True,json.loads(dumps(res))]
        except Exception,e:
            return [False,e]

    def getregexFilter(self,database,collection,key,patt,ty):
        #db.collectionname.find({'files':{'$regex':'^File
        try:
            db=self.client[database]
            if ty=="starts":
                res=db[collection].find({key:{'$regex':'^'+patt}})
            elif ty=="ends":
                res=db[collection].find({key:{'$regex':patt+'$'}})
            elif ty=="contains":
                res=db[collection].find({key:{'$regex':".*"+patt+".*"}})
            else:
                res=db[collection].find({key:{"$eq": patt}})
            return [True,json.loads(dumps(res))]
        except Exception,e:
            return [False,e]

    def getconditionFilter(self,database,collection,key,ty,value):
        try:
            db=self.client[database]
            if ty=="less":
                res=db[collection].find({key:{'$lt':value}})
            elif ty=="equal":
                res=db[collection].find({key:{'$eq':value}})
            else:
                res=db[collection].find({key:{'$gt':value}})
            return [True,json.loads(dumps(res))]
        except Exception,e:
            return [False,e]

class listenToItem(StreamListener):

    def on_data(self, data):
        try:
            #print(data)
            db=DBhandler()
            db.createConnection(username='',password='',port=27017)
            db.insert("innodb","tweets",data)
            #print(data)
            db.closeConnection()
        except Exception,e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        pass


class addItemToTrack():
    def add(self,value):
        try:
            consumer_key = '8rYxIg0LYczfIXqDFWOeoHuOk'
            consumer_secret = '0laLyFydbG5yRqMchWJ1VqOTzDYHaxCQLMSHDsaqZb3Mg6rdeA'
            access_token = '2900259488-ujnZMsE0CCGZbaIZfv2wjMsEGuU2dyItgTtxoZM'
            access_token_secret = 'Kxv1R1Twob6kp4uXGNkNHeyA9V5pkVL6W67WCGbvpcFG4'
            # OAuth process, using the keys and tokens
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            twitter_stream = Stream(auth, listenToItem())
            twitter_stream.filter(track=[value],async=True)
            return True
        except Exception,e:
            print(e)
            return e

class TwitterAPI:
    consumer_key = '8rYxIg0LYczfIXqDFWOeoHuOk'
    consumer_secret = '0laLyFydbG5yRqMchWJ1VqOTzDYHaxCQLMSHDsaqZb3Mg6rdeA'
    access_token = '2900259488-ujnZMsE0CCGZbaIZfv2wjMsEGuU2dyItgTtxoZM'
    access_token_secret = 'Kxv1R1Twob6kp4uXGNkNHeyA9V5pkVL6W67WCGbvpcFG4'
    def __init__(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        pass

    def getTrendsByName(self,id=1):
        globaltrends=self.api.trends_place(id)
        trends= [t["name"] for t in globaltrends[0]["trends"]]
        return trends
        pass


    def getTrends(self,id=1):
        try:
            globaltrends=self.api.trends_place(id)
            return [True,[t["name"] for t in globaltrends[0]["trends"]]]
        except Exception,e:
            print(e)
            return [False,e]

    def searchTweet(self,query='',lang='',locale='',geocode='',result_type='',
                    count='',until='',since_id='',max_id=''):
        try:
            search_results = self.api.search(q=query,lang=lang,locale=locale,geocode=geocode,
            result_type=result_type,count=count,until=until,since_id=since_id,max_id=max_id,)
            data=[i._json for i in search_results]
            #return [True,search_results[0]._json]
            return [True,data]
        except Exception,e:
            print(e)
            return [False,e]

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1/add', methods=['GET'])
def addItemToListen():
    try:
        item = request.args.get('q')
        add=addItemToTrack()
        ret=add.add(item)
        if ret:
            return jsonify({"status":"success","item added:":item})
        else:
            return jsonify({"status":"falied","debug:":ret})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})


@app.route('/api/v1/live', methods=['GET'])
def searchLive():
    try:
        item = request.args.get('q')
        tapi=TwitterAPI()
        ret=tapi.searchTweet(query=item)
        print(ret[0])
        if ret[0]:
            return jsonify({"status":"success","response:":ret[1]})
        else:
            return jsonify({"status":"failed","debug:":ret[1]})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})

@app.route('/api/v1/trends', methods=['GET'])
def getLiveTrends():
    try:
        item = request.args.get('id')
        tapi=TwitterAPI()
        ret=tapi.getTrends(id=item)
        print(ret[0])
        if ret[0]:
            return jsonify({"status":"success","response:":ret[1]})
        else:
            return jsonify({"status":"failed","debug:":ret[1]})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})

@app.route('/api/v1/tweets', methods=['GET'])
def getItemTweets():
    try:
        item = request.args.get('q')
        db=DBhandler()
        db.createConnection(username='',password='',port=27017)
        ret=db.getdata("innodb","tweets")
        db.closeConnection()
        print(ret[0])
        if ret[0]:
            return jsonify({"status":"success","response:":ret[1]})
        else:
            return jsonify({"status":"failed","debug:":ret[1]})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})

@app.route('/api/v1/tweets/sorted', methods=['GET'])
def getSortedItemTweets():
    try:
        item1 = request.args.get('key')
        item2 = request.args.get('reverse')
        db=DBhandler()
        db.createConnection(username='',password='',port=27017)
        ret=db.getSortedData("innodb","tweets",item1,item2)
        db.closeConnection()
        if ret[0]:
            return jsonify({"status":"success","response:":ret[1]})
        else:
            return jsonify({"status":"failed","debug:":ret[1]})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})

@app.route('/api/v1/tweets/range', methods=['GET'])
def getrangeTweet():
    try:
        item1 = request.args.get('key')
        item2 = request.args.get('reverse')
        item3 =  request.args.get('value')
        db=DBhandler()
        db.createConnection(username='',password='',port=27017)
        ret=db.getrangeFilter("innodb","tweets",item1,item2,item3)
        db.closeConnection()
        if ret[0]:
            return jsonify({"status":"success","response:":ret[1]})
        else:
            return jsonify({"status":"failed","debug:":ret[1]})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})

@app.route('/api/v1/tweets/cond', methods=['GET'])
def getcondTweets():
    try:
        item1 = request.args.get('key')
        item2 = request.args.get('condition')
        item3 =  request.args.get('value')
        db=DBhandler()
        db.createConnection(username='',password='',port=27017)
        ret=db.getcondFilter("innodb","tweets",item1,item2)
        db.closeConnection()
        if ret[0]:
            return jsonify({"status":"success","response:":ret[1]})
        else:
            return jsonify({"status":"failed","debug:":ret[1]})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})

@app.route('/api/v1/tweets/regex', methods=['GET'])
def getregexTweets():
    try:
        item1 = request.args.get('key')
        item2 = request.args.get('patt')
        item3 =  request.args.get('type')
        db=DBhandler()
        db.createConnection(username='',password='',port=27017)
        ret=db.getregexFilter("innodb","tweets",item1,item2,item3)
        db.closeConnection()
        if ret[0]:
            return jsonify({"status":"success","response:":ret[1]})
        else:
            return jsonify({"status":"failed","debug:":ret[1]})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})

@app.route('/api/v1/download', methods=['GET'])
def sendFile():
    #content = str(request.form['jsonval'])
    try:
        item1 = request.args.get('db')
        db=DBhandler()
        db.createConnection(username='',password='',port=27017)
        ret=db.getdata("innodb","tweets")
        db.closeConnection()
        content=ret[1]
        return Response(json.dumps(content),
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename=download.json'})
    except Exception,e:
        return jsonify({'status':"failed","debug":str(e)})


if __name__ == '__main__':
    app.run(debug=True)
