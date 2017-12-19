# inno

requirements:
<br>
mongodb
<br>
Flask
<br>
pymongo
<br>
python 2.7
<br>
tweepy
<br>
api endpoints:
<br>
@app.route('/api/v1/add', methods=['GET'])  q(add item to streamlistener)
<br>
@app.route('/api/v1/download', methods=['GET']) q(to download a collection)
<br>
@app.route('/api/v1/tweets/regex', methods=['GET']), key,pattern(substring),type(starts,ends,equal,contains)
<br>
@app.route('/api/v1/tweets/cond', methods=['GET']) ,key,condition(< > ==),value<br>
@app.route('/api/v1/tweets/range', methods=['GET']) key() , start (being value), end(higher value)<br>
@app.route('/api/v1/tweets/sorted', methods=['GET']) key(key to sort upon), reverse(set true to sort in reverse order)<br>
@app.route('/api/v1/tweets', methods=['GET']) q(get tweets of tweet)<br>
@app.route('/api/v1/trends', methods=['GET']) id(geolocation default 1)<br>
@app.route('/api/v1/live', methods=['GET']) q(trend to search)<br>
@app.route('/api/v1/add', methods=['GET'])  q (trend to add)<br>
<br>
improvements:
<br>
cache implementation
<br>
seperate collection for seperate trend(item)
