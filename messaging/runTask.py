#!flask/bin/python



from celery import Celery

from celery import group

from flask import Flask, jsonify, redirect, url_for

import subprocess

import sys

import os

import swiftclient.client

import json

import time

from collections import Counter

dicstatus = {"Status":"initialization..."}
app = Flask(__name__)
#app.secret_key = 'some_secret'

@app.route('/parse', methods=['GET'])
def cow_say():
        config = {'user':os.environ['OS_USERNAME'],
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

        conn = swiftclient.client.Connection(auth_version=2, **config)

        tweets = []
        (res,tweetsObject) = conn.get_container("tweets")
        for t in tweetsObject:
                tweets.append(t["name"])

        aA = tweets[:4]
        aB = tweets[4:8]
        aC = tweets[8:12]
        aD = tweets[12:16]
        aE = tweets[16:]

        A = tweets[:1]
        B = tweets[1:2]
        C = tweets[2:3]
        D = tweets[3:4]
        E = tweets[4:5]

    job = group(parseTweets.s(A),

                parseTweets.s(B),

                parseTweets.s(C),

                parseTweets.s(D),

                parseTweets.s(E))



        global tweetTask

        tweetTask = job.apply_async()

        print "Celery is working..."

        return redirect(url_for('status'))



        #counter = 0

        #while (tweetTask.ready() == False):

        #       print "... %i s" %(counter)

        #       status["Status"] = "... %i s" %(counter) 

        #       counter += 5

        #       time.sleep(5)

#       print "The task is done!"

#       status["Status"] = "DONE!"

#       toReturn = tweetTask.get()



#       c = Counter()

#       for d in toReturn:

#               c.update(d)



#       return jsonify(dict(c)), 200



@app.route('/status', methods=['GET'])
def status():
        if (tweetTask.ready() == False):
#               print "... %i s" %(counter)
                dicstatus["Status"] ="PENDING"
        #       time.sleep(5)
                return jsonify(dicstatus), 200

        print "The task is done!"
       #status["Status"] = "DONE!"
        toReturn = tweetTask.get()
        c = Counter()
        for d in toReturn:
                c.update(d)

        return jsonify(dict(c)), 200

#       return jsonify(status), 200

if __name__ == '__main__':
        app.run(host='0.0.0.0',debug=True)
