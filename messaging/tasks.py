from celery import Celery
app = Celery('tasks', backend='amqp', broker='amqp://')
@app.task(ignore_result=True)
def print_hello():
    print 'hello there'


@app.task
def parseTweets():
	import os
	import swiftclient.client
	import json
	config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

	conn = swiftclient.client.Connection(auth_version=2, **config)

	pronoms=["han", "hon", "den", "det", "denna", "denne", "hen"] 
	pronoms_count= [0,0,0,0,0,0,0]

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
				tmp = json.loads(line)["text"].split()
				retweet = json.loads(line)["retweeted"]
				if retweet == False:
					for i in range(len(pronoms)):
						if(pronoms[i] in tmp):
							pronoms_count[i] += 1
			except:
				pass
		objects.close()
	for i in range(len(pronoms)):
		print "Antal %s: %i" %(pronoms[i], pronoms_count[i])