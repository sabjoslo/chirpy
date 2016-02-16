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
import logging
from configModule import read_config

configs = read_config()
ppath = configs['ppath']
lpath = configs['lpath']
root = configs['dpath']
if root == 'False':
	root = './'

def user_setup(output_dir, logfile):
        print 'Getting Configurations'
        logging.info('Getting Configurations')
        time.sleep(0.5)

        if output_dir: helpModule.make_outdir(root+output_dir)
	open(logfile, 'a')

  	print 'Retrieving Twitter Profile'
        logging.info('Retrieving Twitter Profile')
        time.sleep(0.5)
	global __profile
        __profile = profileModule.get_profile(ppath, lpath)
	logging.debug('Using profile '+__profile.upper())
        profilepath = ppath+__profile+'.profile'
        deets = profileModule.get_deets(profilepath)
	helpModule.write_header('chirpy '+' '.join(sys.argv[1:]), __profile, logfile)

        print 'Authorizing Twitter Profile'
        logging.info('Authorizing Twitter Profile')
        time.sleep(0.5)
        auth = tweepy.OAuthHandler(deets["consumer_key"], deets["consumer_secret"])
        auth.set_access_token(deets["access_token"], deets["access_token_secret"])
        global __twitterapi__
	__twitterapi__ = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
	
def get_user_timeline(user_id, user, count, include_rts, max_id=None):
	if user_id:
		return __twitterapi__.user_timeline(user_id=user, count=count, max_id=max_id, include_rts=include_rts)
	else:
		return __twitterapi__.user_timeline(screen_name=user, count=count, max_id=max_id, include_rts=include_rts)

def user_history(user, fo, output_dir, num, rts, overwrite, logfile):	
	if num > 3200:
		print 'Twitter only allows access to the last 3,200 user tweets.'
		loop = True
		while loop: 
			new_num = raw_input('Enter another integer, or hit enter to continue.')
			loop = False
			if new_num.strip():
				if new_num.isdigit():
					num = int(new_num)
					loop = False
				else:
					print 'Integer required.'
					logging.error('num_tweets not an integer')
					loop = True
	if num > 3200:
		print 'Twitter only allows access to the last 3,200 user tweets.'
		

	write_to_file = True
	if fo:
		outfile = root + fo
	elif output_dir:
		outfile = root + '/' + output_dir + '/' + user+'.txt'
	else:
		outfile = sys.stdout
		write_to_file = False
	

	print 'Configuring Files'
	logging.info('Configuring Files')
	time.sleep(0.5)

	if overwrite and write_to_file:
		fo = open(outfile, 'w')
		logging.info('Creating empty file '+outfile)
		fo.close()
	
	count = 200
	status = []

	print 'Extracting User Tweets'
	logging.info('Extracting User Tweets')
	time.sleep(0.5)
	if num < count:
		timeline_results = get_user_timeline(user.isdigit(), user, num, rts)
	else:
		timeline_results = get_user_timeline(user.isdigit(), user, count, rts)

   	status.extend(timeline_results)
	helpModule.write_to_log_file(len(status), __profile, user, logfile)
	helpModule.write_timestamp(user, len(status), rts, write_to_file, outfile)
	logging.info('Writing to file '+str(outfile))
	for item in status:
		helpModule.write_to_file(item, write_to_file, outfile)
		time.sleep(1)
	logging.info(str(len(status))+' Tweets written to output')
	logging.debug('[0:'+str(len(status)-1)+'] written to output.')
	print 'Tweets Collected: ', len(status)
	oldest = status[-1]['id'] - 1

	while len(timeline_results) > 0 and len(status) < num:
		last_ent = status[-1]
		left_to_go = num - len(status)
		if left_to_go < count:
			timeline_results = get_user_timeline(user.isdigit(), user, left_to_go, rts, oldest)
		else:
			timeline_results = get_user_timeline(user.isdigit(), user, count, rts, oldest)
        	status.extend(timeline_results)
		oldest_ix = status.index(last_ent)
		logging.info('Writing to file '+str(outfile))
		print 'Writing To File'
		for item in status[oldest_ix+1:]:
			helpModule.write_to_file(item, write_to_file, outfile)
			time.sleep(1)
		logging.debug('['+str(oldest_ix+1)+':'+str(len(status)-1)+'] written to output.')
		logging.info(str(len(status))+' Tweets written to output')
        	oldest = status[-1]['id'] - 1

        	print 'Tweets Collected: ', len(status)
               
		helpModule.write_to_log_file(len(status), __profile, user, logfile)

		time.sleep(6)

	if num > len(status):
		print 'Could not retrieve number specified.'
		logging.warning('Could not retrieve num_tweets specified')

	logging.info('Process completed')

	return

