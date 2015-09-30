#!flask/bin/python
from flask import Flask, jsonify
import subprocess
import sys

app = Flask(__name__)


@app.route('/Labb3/messaging/', methods=['GET'])
def cow_say():
    from tasks import parseTweets

	tweets = parseTweets.delay()
    
    return tweets

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)