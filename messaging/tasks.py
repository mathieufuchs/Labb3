from celery import Celery
app = Celery('tasks', backend='amqp', broker='amqp://')
@app.task(ignore_result=True)
def print_hello():
    print 'hello there'
@app.task
def gen_prime(x):
    multiples = []
    results = []
    for i in xrange(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in xrange(i*i, x+1, i):
                multiples.append(j)
    return results
@app.task
def parseTweets():
	import json
	pronoms=["han", "hon", "den", "det", "denna", "denne", "hen"] 
	pronoms_count= [0,0,0,0,0,0,0]
	objects = open('tweetsTemp.txt', 'w')
	objects.write(obj[1])
	objects.close()
	objects = open('tweetsTemp.txt', 'r')
	for line in objects:
	    try:
	        tmp = json.loads(line)["text"]
	        retweet = json.loads(line)["retweeted"]
	        if retweet == false:
	        	for i in range(len(pronoms)):
	            	if(pronoms[i] in tmp):
	                	pronoms_count[i] += 1
	    except:
	        pass
	for i in range(len(pronoms)):
	    print "Antal %s: %i" %(pronoms[i], pronoms_count[i])
	objects.close()