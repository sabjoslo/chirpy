#!/usr/bin/env python

__author__ = 'SaleemSaddm'

import os
import sys
import shutil
import codecs
if sys.stdout.encoding == None:
	os.putenv("PYTHONIOENCODING",'UTF-8')
	os.execv(sys.executable,['python']+sys.argv)

sys.dont_write_bytecode = True

x = os.path.dirname(os.path.realpath(__file__))

#-------------------------------------------------------------------------------------------------------------

from logModule import ref_logs
from configModule import read_config
import profileModule
from searchModule import searching
from userModule import user_setup, user_history
import parseModule
import streamModule
import helpModule

import argparse
import signal
import subprocess
import ConfigParser
import tweepy
import sys
import logging
import json
from ChirpyError import *
import fileinput
import traceback
import select

configs = read_config()
#ref_logs() function deletes log files from previous processes.
ref_logs(configs['lpath'])

#-------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("options", help = "Available: search, user, stream, stream_list, stream_remove, profile_add, profile_list, profile_remove, tophash, parse, cleanup")
parser.add_argument("-i", "--in", help="input file", action="store", dest = 'input_file')
parser.add_argument("-f", "--fo", help="output file", action="store", dest = 'output_file')
parser.add_argument("-o", "--op", help="output dir", action="store", dest = 'output_dir')
parser.add_argument("-k", "--kw", help="keyword", action="store", dest = 'query')
parser.add_argument("user", type=str, nargs="*", help="Twitter user(s) (can be screen name or user ID", action="store")
parser.add_argument("-n", "--nm", help="tweet limit / hashtag count", action="store", default=3200, type=int, nargs="?", dest = 'num')
parser.add_argument("--retweets", help="include retweets in user timeline", action="store_const", const=True, default=False, dest = 'rts')
parser.add_argument("-u, --update", help="Update policy. Options: APPEND (append user data to existing files), OVERWRITE (overwrite users with existing file), SKIP (skip users with existing file)", action="store", default="APPEND", dest = 'update')
parser.add_argument("-d", "--dy", help="number of days", action="store", dest = 'days')
parser.add_argument("-p", "--pd", help="process id", action="store", dest = 'pid')
parser.add_argument("-l", "--log", help="logging level", action="store", default="warning", dest='llevel')
parser.add_argument("-pi", help="Process ID of process to resume", action="store", dest='pi')
parser.add_argument("--nosweep", help="Tells Chirpy not to clean up event log after session", action="store_const", const=True, default=False, dest='nosweep')
args = parser.parse_args()

#-------------------------------------------------------------------------------------------------------------

pid = str(os.getpid())
sessionlog = configs['lpath']+'/'+pid+'.eventlog'
llevel = args.llevel.upper()
logging.basicConfig(filename=sessionlog, level=llevel, format='%(asctime)s: \
	%(name)s:  %(levelname)s: %(message)s')

if args.options == 'search':
	logging.info('Search module called')
	
	if args.query:
		query = args.query
	elif not sys.stdin.isatty():
		logging.info('Reading from stdin.')
		for q in sys.stdin[0]:
			query = q.rstrip('\n').rstrip('\r')
		if len(query) == 0:
			raise InputError('stdin is empty.', llevel = 'critical')
	else:
		raise InputError('Missing parameters. Requires -k keyword.')

	write_to_file = False
	if args.output_file:
		if args.output_dir:
			output_file = args.output_dir + '/' + args.output_file
		else:
			output_file = args.output_file
		write_to_file = True
	else:
		output_file = sys.stdout
		
	if args.num:
		num = args.num
	else:
		num = 0

	searching(configs, query, write_to_file, output_file, num)	


elif args.options == 'user':
	logging.info('User module called')

	if not args.user:
		if sys.stdin.isatty():
			print 'No user passed.'
			raise InputError('Requires user.', llevel='critical')

	output_file = False
	output_dir = False
	if args.output_file:
		output_file = args.output_file
	 	output = output_file
	elif args.output_dir:
              	output_dir = args.output_dir
		output = output_dir + '/<userid>_<screenname>.txt'
	else:
		output = 'stdout'
      
	num = args.num
	rts = args.rts
	if args.update.lower() in ['append', 'overwrite', 'skip']:
		update = args.update.upper()
	else:
		update = 'APPEND' 
		
	lpath = configs['lpath']
	logfile = lpath+pid+'.userlog'
        print 'Output written to ', output
        print 'Number of tweets: ', num
        print 'Include retweets: ', rts
        print 'Update: ', update
 			
	user_setup(output_dir, logfile)
	
	if not sys.stdin.isatty():
		user = sys.stdin.readline().rstrip()
		print user
		while user.strip():
			print 'Current user: '+user
                       	try:
                        	user_history(user, output_file, output_dir, num, rts, update, logfile)
                        except tweepy.error.TweepError as e:
                                print e
                                logging.warning('TweepyError: '+str(e))   
			user = sys.stdin.readline().rstrip()
		else:
			raise InputError('No user passed.', llevel='error')

	else:
		users = args.user
		for user in users:
			print 'Current user: '+user
			try:
                     		user_history(user, output_file, output_dir, num, rts, update, logfile)
			except tweepy.error.TweepError as e:
				print e
				logging.warning('TweepyError: '+str(e))
				continue
	
	helpModule.delete_file(logfile)			

elif args.options == 'parse':
	logging.info('Calling create_csv() from parseModule')
        if not args.input_file:
                print 'Missing Parameters'
                print 'Requires -i input file and optional -f ouput file -u user -k keyword'
		logging.error('Missing Parameters')

        else:
		infile = args.input_file

		if args.output_file:
			outfile = args.output_file
		else:
			outfile = infile.split('.')[0]+'_csvfile.csv'

		if args.query:
			query = args.query
		else:
			query = False

		if args.user:
			uname = args.user
		else:
			uname = False

		parseModule.create_csv(infile, outfile, query, uname)

elif args.options == 'tophash':
	logging.info('Calling hash_list() from parseModule')
	if not args.input_file:
                print 'Missing Parameters'
                print 'Requires -i input file and optional -n number of hashtags'
		logging.error('Missing parameters')		

        else:
                infile = args.input_file

                if args.num:
                        num = args.num
                else:
                        num = 100

                parseModule.hash_list(infile, num)

elif args.options == 'profile_list':
	logging.info('Profile list requested')
	profileModule.plist(configs['lpath'], configs['ppath'])
	
elif args.options == 'profile_add':
	logging.info('Profile add request')
        profileModule.padd(configs['ppath'])

elif args.options == 'profile_remove':
	logging.info('Profile remove request')
        profileModule.pdel(configs['ppath'])

elif args.options == 'stream':
	logging.info('Starting stream.')
        if not args.days or not args.query or not args.output_dir or not args.output_file:
                print 'Missing Parameters'
                print 'Requires -k keyword, -o ouputdir, -d number of days, -f output file '
		logging.error('Missing parameters.')
        else:
                print 'Stream Started'
		logging.info('Stream started.')
		subprocess.Popen(['python', x+'/streamer.py', '-d', args.days, '-o', args.output_dir, '-f', args.output_file, '-k', args.query])

elif args.options == 'stream_list':
	logging.info('Getting stream list.')
        streamModule.list_runs(configs['lpath'])

elif args.options == 'stream_remove':
	logging.info('Removing stream.')
        if not args.pid:
                print 'Missing Parameters'
                print 'Requires -p pid'
		logging.error('Missing parameters.')
        else:
                streamModule.kill_p(args.pid, configs['lpath'])

elif args.options == 'cleanup':
	logging.info('Cleaning up logs.')
	ref_logs(configs['lpath'])

else:
        print args.options, ': Command Not Found, check chirpy --help for the available options'
        sys.exit()

logging.shutdown()
if not args.nosweep:
	os.remove(sessionlog)
