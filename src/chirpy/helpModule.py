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
	except OSError as exception:
                if exception.errno != errno.EEXIST:
                        raise
			logging.error('Creating '+path+' throws OSError')
			
