#!flask/bin/python

from celery import Celery
from flask import Flask, jsonify
import subprocess
import sys
import os
import swiftclient.client
import json
import time
from collections import Counter
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

	pronoms={"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0} 

	#tweets = conn.get_container("tweets")[1]
	#tweets = tweets[0:1]
	tweets = [{"name":"tweets_19.txt"}]
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
	config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

	conn = swiftclient.client.Connection(auth_version=2, **config)

	tweets = conn.get_container("tweets")[1]

	A = tweets[:4]
	B = tweets[4:8]
	C = tweets[8:12]
	D = tweets[12:16]
	E = tweets[16:]

	job = group(parseTweets.s(A["name"]), 
		parseTweets.s(B["name"]), 
		parseTweets.s(C["name"]),
		parseTweets.s(D["name"]),
		parseTweets.s(E["name"]))

	tweetTask = job.apply_async()
	print "Celery is working..."
	counter = 0
	while (tweetTask.ready() == False):
		print "... %i s" %(counter)
		counter += 5
		time.sleep(5)
	print "The task is done!"

	toReturn = tweetTask.get()

	c = Counter()
	for d in toReturn:
    	c.update(d)

	return jsonify(dict(c)), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

