'''
@uthor: Haji Mohammad Saleem

Helper module for Harvest
'''

import os, json
import errno
import time
from datetime import datetime
import logging

#------------------------------------------------------------------------

def write_timestamp(user, num, rts, write_to_file, filepath):
	if write_to_file:
		fo = open(filepath, 'a')
	else:
		fo = filepath
	now = datetime.now()
	fo.write(json.dumps({user: {"created-on": now.strftime("%d/%m/%Y at %H:%M:%S"), "num_tweets": str(num), "retweets": rts}}))
	fo.write('\n')
	return

def write_header(label, string, filepath):
	with open(filepath, 'a') as fo:
		fo.write(json.dumps({label: string}))
	return

def write_to_log_file(n, profile, user, filepath):
	with open(filepath, 'r+') as fo:
		log = json.load(fo)
		log["profile"] = profile
		log[user] = {"tweets_collected": n}
		fo.seek(0)
		json.dump(log, fo, indent=4)
	return

def delete_file(filepath):
	logging.info('Deleting '+filepath)
	os.remove(filepath)

def write_to_file(jsonlist, write_to_file, filepath):
        if write_to_file:
		fo = open(filepath, 'a')
	else:
		fo = filepath
        for item in jsonlist:
        	fo.write(json.dumps(item))
                fo.write('\n')
        return

def make_outdir(path):
        try:
                os.makedirs(path)
        	print 'Output Directory Created'
		time.sleep(0.5)
	except OSError as exception:
                if exception.errno != errno.EEXIST:
                        raise
			logging.error('Creating '+path+' throws OSError')
			
