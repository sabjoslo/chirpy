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

        if output_dir: helpModule.make_outdir(root+output_dir)

  	print 'Retrieving Twitter Profile'
        logging.info('Retrieving Twitter Profile')
	global __profile
        __profile = profileModule.get_profile(ppath, lpath)
	logging.debug('Using profile '+__profile.upper())
        profilepath = ppath+__profile+'.profile'
        deets = profileModule.get_deets(profilepath)

	with open(logfile, 'a') as fo:
                fo.write(__profile+'\n')

        print 'Authorizing Twitter Profile'
        logging.info('Authorizing Twitter Profile')
        auth = tweepy.OAuthHandler(deets["consumer_key"], deets["consumer_secret"])
        auth.set_access_token(deets["access_token"], deets["access_token_secret"])
        global __twitterapi__
	__twitterapi__ = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
	
def get_user_timeline(user_id, user, count, include_rts, max_id=None):
	try:
		if user_id:
			return __twitterapi__.user_timeline(user_id=user, count=count, max_id=max_id, include_rts=include_rts)
		else:
			return __twitterapi__.user_timeline(screen_name=user, count=count, max_id=max_id, include_rts=include_rts)
	except tweepy.error.RateLimitError as e:
		print e
		logging.error('RateLimitError.')

def user_history(user, output_file, output_dir, num, rts, update, logfile):	
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

	if user.isdigit():
		userid = user
	else:
		logging.debug('Calling API to get ID for user '+user)
		userid = __twitterapi__.get_user(screen_name = user)['id_str']
        if update == 'SKIP' and output_dir:
                for f in os.listdir(output_dir):
                        if f.split('_')[0] == userid:
                                print 'Skipping user #'+userid
                                logging.info('Skipping user #'+userid)
                                return

	print 'Configuring Files'
	logging.info('Configuring Files')
	
	count = 200
	status = []

	print 'Extracting User Tweets'
	logging.info('Extracting User Tweets')
	if num < count:
		timeline_results = get_user_timeline(user.isdigit(), user, num, rts)
	else:
		timeline_results = get_user_timeline(user.isdigit(), user, count, rts)

	with open(logfile, 'a') as fo:
		fo.write(user+'\n')
		fo.write(str(len(status))+'\n')
	
	if timeline_results is not None:
 	  	status.extend(timeline_results)
		oldest = status[-1]['id'] - 1
	
		screenname = status[0]['user']['screen_name']
		print screenname

		print 'Tweets Collected: ', len(status)

	while len(timeline_results) > 0 and len(status) < num:
		left_to_go = num - len(status)
		if left_to_go < count:
			timeline_results = get_user_timeline(user.isdigit(), user, left_to_go, rts, oldest)
		else:
			timeline_results = get_user_timeline(user.isdigit(), user, count, rts, oldest)
        	status.extend(timeline_results)
        	oldest = status[-1]['id'] - 1

        	print 'Tweets Collected: ', len(status)
               
		with open(logfile, 'a') as fo:
			fo.write(str(len(status))+'\n')

	if num > len(status):
		print 'Could not retrieve number specified.'
		logging.warning('Could not retrieve num_tweets specified')

	if len(status) > 0:
		write_to_file = True
       		if output_file:
               		outfile = root + output_file
        	elif output_dir:
                	outfile=root+'/'+output_dir+'/'+userid+'_'+screenname+'.txt'
        	else:
                	outfile = sys.stdout
                	write_to_file = False

		if update == 'OVERWRITE' and write_to_file:
                	fo = open(outfile, 'w')
                	logging.info('Creating empty file '+outfile)
                	fo.close()

		print 'Writing To File'
		logging.info('Writing to file '+str(outfile))
		helpModule.write_timestamp(user, len(status), rts, write_to_file, outfile)
		helpModule.write_to_file(status, write_to_file, outfile)
	else:
		print 'No Tweets collected.'
	
	logging.info('Process completed')

	return

