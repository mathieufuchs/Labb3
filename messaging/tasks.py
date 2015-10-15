from celery import Celery
import os
import swiftclient.client
import json
import urllib2
app = Celery('tasks', backend='amqp', broker='amqp://ma:fu@130.238.29.120/mafu')

@app.task()
def parseTweets(tweetName):

	pronoms={"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0}
	n = 0 

	#tweets = conn.get_container("tweets")[1]
	#tweets = tweets[0:1]
	#tweets = [{"name":"tweets_19.txt"}]
	for t in tweetName:
		print t
		req = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/" + t)
		response = urllib2.urlopen(req)
		obj = response.read()
		objects = open(t, 'w')
		objects.write(obj)
		objects.close()
		objects = open(t, 'r')
		for line in objects:
			try:
				jL = json.loads(line)
				tmp1 = jL["text"].lower()
				tmp = tmp1.split()
				retweet = jL["retweet_count"]
				if retweet == 0:
					n += 1
					for i in pronoms.keys():
						if(i in tmp):
							pronoms[i] += 1
			except:
				pass
		objects.close()
	pronoms.update({"num_of_tweets": n})
	return pronoms