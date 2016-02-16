#!/usr/bin/python


import os, sys, shutil, codecs
if sys.stdout.encoding == None:
    os.putenv("PYTHONIOENCODING",'UTF-8')
    os.execv(sys.executable,['python']+sys.argv)

#-------------------------------------------------------------------------------------------------------------

import profileModule
import helpModule
import datetime
from urllib import quote_plus
from urllib import unquote
import json, time, errno
import twitter
import logging

def searching(configs, query, write_to_file, output_file, num):
	print 'Getting Configurations'
	logging.info('Getting configurations')
	time.sleep(0.5)
	ppath = configs['ppath']
	lpath = configs['lpath']
	root = configs['dpath']
	if root == 'False':
        	root = './'
	
	print 'Configuring Files'
	logging.info('Configuring files')
	time.sleep(0.5)
	if write_to_file:
		outfile = root + output_file
		fo = open(outfile, 'w')
		fo.close()
	else:
		outfile = output_file

	print 'Encoding Query'
	logging.info('Encoding Query')
	time.sleep(0.5)
	enc_query = quote_plus(query.encode('UTF-8'), safe=':/')

        pid = str(os.getpid())
        logfile = lpath+pid+'.searchlog'
	
	print 'Retrieving Twitter Profile'
	logging.info('Retrieving Twitter Profile')
        time.sleep(0.5)
	profile = profileModule.get_profile(ppath, lpath)
        profilepath = ppath+profile+'.profile'
        deets = profileModule.get_deets(profilepath)

	print 'Authorizing Twitter Profile'
	logging.info('Authorizing Twitter profile')
	time.sleep(0.5)
	auth = twitter.oauth.OAuth(deets["access_token"], deets["access_token_secret"], deets["consumer_key"], deets["consumer_secret"])
	twitter_api = twitter.Twitter(auth=auth)

	count = 100

	print 'Starting Search'
	logging.info('Starting search')
	time.sleep(0.5)
	search_results = twitter_api.search.tweets(q=enc_query, count=count)

	with open(logfile, 'a') as fo:
		fo.write(profile+'\n')
		fo.write(query+'\n')

	statuses = search_results['statuses']
	counter = 0
	tweets = 0

	while True:
		counter+=len(statuses)
		print "Tweets Collected: ", counter
 
		if int(num)!= 0 and counter >= int(num):
			print 'Deadline Reached \nExiting'
			logging.info('Deadline reached. No more Tweets collected.')
			break		

		helpModule.write_to_file(statuses, outfile)
		statuses = []

		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e:
			break

		kwargs = dict([ kv.split('=') for kv in unquote(next_results[1:]).split("&") ])

		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']

		with open(logfile, 'a') as fo:
			fo.write(str(tweets)+'\n')

		time.sleep(6)

	print 'Writing To File'
	if write_to_file:
		out = output_file
	else:
		out = 'stdout'
	logging.info('Writing to '+out)
	helpModule.write_to_file(statuses, write_to_file, outfile)

	os.remove(logfile)
	
	logging.info('Process complete.')

	return

