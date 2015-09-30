#!flask/bin/python

from celery import Celery
from flask import Flask, jsonify
import subprocess
import sys
import os
import swiftclient.client
import json
import time
appC = Celery('tasks', backend='amqp', broker='amqp://')
@appC.task(ignore_result=True)
def print_hello():
	print 'hello there'


@appC.task
def parseTweets():
	
	config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

	conn = swiftclient.client.Connection(auth_version=2, **config)

	pronoms={"han":0 , "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0} 

	tweets = conn.get_container("tweets")[1]
	for t in tweets:
		print t["name"]
		obj = conn.get_object("tweets", t["name"])
		objects = open('tweetsTemp.txt', 'w')
		objects.write(obj[1])
		objects.close()
		objects = open('tweetsTemp.txt', 'r')
		for line in objects:
			try:
				tmp1 = json.loads(line)["text"].lower()
				tmp = tmp1.split()
				retweet = json.loads(line)["retweet_count"]
				if retweet == 0:
					for i in pronoms.keys():
						if(i in tmp):
							pronoms[i] += 1
			except:
				pass
		objects.close()
	return pronoms



app = Flask(__name__)

@app.route('/Labb3/messaging', methods=['GET'])
def cow_say():
    tweets = parseTweets.delay()
    while(tweets.ready() == False):
    	print "celery is working"
    	time.sleep(5)
	return jsonify(tweets), 200
if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

