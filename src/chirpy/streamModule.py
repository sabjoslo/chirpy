#!/usr/bin/python

#-------------------------------------------------------------------------------------------------------------

import signal
from prettytable import PrettyTable
import os
import time 

#-------------------------------------------------------------------------------------------------------------

def kill_p(pid, lpath):
        fname = lpath+str(pid)+'.streamlog'
	if os.path.isfile(fname):
		with open(fname, 'r') as fo:
			lines = fo.readlines()
		cid = lines[2].rstrip()
		os.kill(int(cid), signal.SIGQUIT) 
		os.kill(int(pid), signal.SIGQUIT) 
		
		print 'Stream terminated'
		logging.info('Stream terminated. Process complete.')
			
	else:
		print 'Stream not found'
		logging.error('Stream not found.')


def list_runs(lpath):
	print 'Running Streams'

        title = ['Pid', 'Query', 'Tweets Collected', 'Run time', 'Profile']

        x = PrettyTable(title)
        x.align["Pid"] = "l"
        x.align["Query"] = "l"
        x.align["Tweets Collected"] = "l"
        x.align["Run Time"] = "l"
        x.align["Profile"] = "l"

        logging.info('Getting streams.')
        lof = os.listdir(lpath)
        for f in lof:
                if 'stream' in f:
			with open(lpath+f, 'r') as fo:
                                a = fo.readlines()

                        pid = f.split('.')[0]
			p = a[0]
                        q = a[1]
                        t = a[-1].split()[1]
                        tm = a[-1].split()[0]
                        x.add_row([pid, q, t, tm, p])
	logging.info('Printing streams.')
        print x
	
	logging.info('Process complete.')
	return

	
