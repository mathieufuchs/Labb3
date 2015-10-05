from celery import Celery
import os
import swiftclient.client
import json
app = Celery('tasks', backend='amqp', broker='amqp://')
@app.task(ignore_result=True)
def print_hello():
    print 'hello there'

"""
names_of_files
for name in name_of_files:


	parseTweets(name)

"""


@app.task()
def parseTweets(tweetName):
	
	config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

	conn = swiftclient.client.Connection(auth_version=2, **config)

	pronoms={"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0}
	n = 0 

	#tweets = conn.get_container("tweets")[1]
	#tweets = tweets[0:1]
	#tweets = [{"name":"tweets_19.txt"}]
	for t in tweetName:
		print t
		obj = conn.get_object("tweets", t)
		objects = open(t, 'w')
		objects.write(obj[1])
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