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

def get_user_timeline(api, user_id, user, count, include_rts, max_id=None):
	if user_id:
		return api.user_timeline(user_id=user, count=count, max_id=max_id, include_rts=include_rts)
	else:
		return api.user_timeline(screen_name=user, count=count, max_id=max_id, include_rts=include_rts)

def user_history(configs, user, fo, output_dir, num, rts, overwrite, logfile):
	print 'Accessing User', user
	time.sleep(0.5)
	print 'Getting Configurations' 
	time.sleep(0.5)
	ppath = configs['ppath']
	lpath = configs['lpath']
	root = configs['dpath']
	if root == 'False':
        	root = './'

	if output_dir: helpModule.make_outdir(root+output_dir)
	
	write_to_file = True
	if fo:
		outfile = root + fo
	elif output_dir:
		outfile = root + '/' + output_dir + '/' + user+'.txt'
	else:
		outfile = sys.stdout
		write_to_file = False
	

	print 'Configuring Files'
	time.sleep(0.5)

	if overwrite and write_to_file:
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
		timeline_results = get_user_timeline(twitter_api, user.isdigit(), user, num, rts)
	else:
		timeline_results = get_user_timeline(twitter_api, user.isdigit(), user, count, rts)

   	status.extend(timeline_results)
	oldest = status[-1]['id'] - 1

	print 'Tweets Collected: ', len(status)

	while len(timeline_results) > 0 and len(status) < num:
		left_to_go = num - len(status)
		if left_to_go < count:
			timeline_results = get_user_timeline(twitter_api, user.isdigit(), user, left_to_go, rts, oldest)
		else:
			timeline_results = get_user_timeline(twitter_api, user.isdigit(), user, count, rts, oldest)
        	status.extend(timeline_results)
        	oldest = status[-1]['id'] - 1

        	print 'Tweets Collected: ', len(status)
               
		helpModule.write_to_log_file(len(status), profile, user, logfile)

		time.sleep(6)

	if num > len(status):
		print 'Could not retrieve number specified. Twitter allows access to last 3,200 tweets.'

	print 'Writing To File'
	helpModule.write_timestamp(user, len(status), rts, write_to_file, outfile)
	helpModule.write_to_file(status, write_to_file, outfile)
	
	return

