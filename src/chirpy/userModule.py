#!/usr/bin/python


import os, sys, shutil, codecs
if sys.stdout.encoding == None:
    os.putenv("PYTHONIOENCODING",'UTF-8')
    os.execv(sys.executable,['python']+sys.argv)

#-------------------------------------------------------------------------------------------------------------

import profileModule
import helpModule
import datetime
import json, time, errno
import tweepy

def user_history(configs, user, output_dir, num, rts, overwrite, logfile):
	print 'Accessing User', user
	time.sleep(0.5)
	print 'Getting Configurations' 
	time.sleep(0.5)
	ppath = configs['ppath']
	lpath = configs['lpath']
	root = configs['dpath']
	if root == 'False':
        	root = './'

	helpModule.make_outdir(root+output_dir)
	
	output_file = user+'.txt'

	print 'Configuring Files'
	time.sleep(0.5)
	outfile = root + output_dir + '/' + output_file

	if overwrite:
		fo = open(outfile, 'w')
		fo.close()
	
	print 'Retrieving Twitter Profile' 
        time.sleep(0.5)
	profile = profileModule.get_profile(ppath, lpath)
        profilepath = ppath+profile+'.profile'
        deets = profileModule.get_deets(profilepath)

	print 'Authorizing Twitter Profile'
	time.sleep(0.5)
	auth = tweepy.OAuthHandler(deets["consumer_key"], deets["consumer_secret"])
    	auth.set_access_token(deets["access_token"], deets["access_token_secret"])
    	twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
	
	count = 200
	status = []

	print 'Extracting User Tweets'
	time.sleep(0.5)
	if num < count:
		timeline_results = twitter_api.user_timeline(screen_name = user, count=num, include_rts=rts)
	else:
		timeline_results = twitter_api.user_timeline(screen_name = user, count=count, include_rts=rts)

   	status.extend(timeline_results)
	oldest = status[-1]['id'] - 1

	print 'Tweets Collected: ', len(status)

	while len(timeline_results) > 0 and len(status) < num:
		left_to_go = num - len(status)
		if left_to_go < count:
			timeline_results = twitter_api.user_timeline(screen_name = user, count=left_to_go, max_id=oldest, include_rts=rts)
		else:
			timeline_results = twitter_api.user_timeline(screen_name = user, count=count, max_id=oldest, include_rts=rts)
        	status.extend(timeline_results)
        	oldest = status[-1]['id'] - 1

        	print 'Tweets Collected: ', len(status)
               
		helpModule.write_to_log_file(len(status), profile, user, logfile)

		time.sleep(6)

	if num > len(status):
		print 'Could not retrieve number specified. Twitter allows access to last 3,200 tweets.'

	print 'Writing To File'
	helpModule.write_timestamp(len(status), rts, outfile)
	helpModule.write_to_file(status, outfile)
	
	return

