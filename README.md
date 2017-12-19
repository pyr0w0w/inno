# inno

requirements:
mongodb
Flask
pymongo
python 2.7
tweepy

api endpoints:
@app.route('/api/v1/add', methods=['GET'])  q(add item to streamlistener)
@app.route('/api/v1/download', methods=['GET']) q(to download a collection)
@app.route('/api/v1/tweets/regex', methods=['GET']), key,pattern(substring),type(starts,ends,equal,contains)
@app.route('/api/v1/tweets/cond', methods=['GET']) ,key,condition(< > ==),value
@app.route('/api/v1/tweets/range', methods=['GET']) key() , start (being value), end(higher value)
@app.route('/api/v1/tweets/sorted', methods=['GET']) key(key to sort upon), reverse(set true to sort in reverse order)
@app.route('/api/v1/tweets', methods=['GET']) q(get tweets of tweet)
@app.route('/api/v1/trends', methods=['GET']) id(geolocation default 1)
@app.route('/api/v1/live', methods=['GET']) q(trend to search)
@app.route('/api/v1/add', methods=['GET'])  q (trend to add)

improvements:
cache implementation
seperate collection for seperate trend(item)
