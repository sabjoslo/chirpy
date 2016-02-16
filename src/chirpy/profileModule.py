'''
@author: Haji Mohammad Saleem
Harvest Module for profile handling

'''
#-----------------------------------------------------------------------------------

import os
import codecs
from prettytable import PrettyTable
import time
import sys
import logging

#-----------------------------------------------------------------------------------

def get_profile(ppath, lpath):
	logging.info('Getting profiles from '+ppath)
        profiles = os.listdir(ppath)

        profiles = [x for x in profiles if '.profile' in x]

        if len(profiles) == 0:
                time.sleep(0.5)
		print 'No Available Profiles. Add A Few.'
		logging.warning('No available profiles.')
                sys.exit()

        pname = [x[:-8] for x in profiles]
        logfiles = os.listdir(lpath)

        used = []

	logging.info('Finding available profiles')
        for f in logfiles:
		if '.eventlog' not in f:
			with open(lpath+f, 'r' ) as fo:
				a = fo.readlines()
			used.append(a[0].rstrip())
        free = list(set(pname).difference(used))

        if free:
                return free[0]
		logging.info('Returning '+free[0])
        else:
                time.sleep(0.5)
		print 'No Free Profiles'
		logging.warning('No free profiles.')
                sys.exit()

def get_deets(profilepath):
    with codecs.open(profilepath, 'r', encoding='UTF-8') as fo:
        info = fo.readlines()

    deets = {}

    logging.info('Getting deets for profile '+profilepath.split('/')[-1])
    for line in info:
        infobit = line.rstrip().split(' ')
        if infobit[0] == 'access_token':
            deets["access_token"] = infobit[2]
        if infobit[0] == 'access_token_secret':
            deets["access_token_secret"] = infobit[2]
        if infobit[0] == 'consumer_key':
            deets["consumer_key"] = infobit[2]
        if infobit[0] == 'consumer_secret':
            deets["consumer_secret"] = infobit[2]

    return deets

def plist(lpath, ppath):
	logging.info('Getting all profiles')
	logdeets = {}

	lof = os.listdir(lpath)
	for f in lof:
		if '.eventlog' not in f:
			with open(lpath+f, 'r') as fo:
				a = fo.readlines()

			p = a[0].rstrip()
			if 'search' in f:
				logdeets[p] = 'search'
			if 'stream' in f:
				logdeets[p] = 'stream'
			if 'user' in f:
                      	 	logdeets[p] = 'user'

	logging.info('Pretty printing all profiles')
	x = PrettyTable(["Profile Name", "Consumer Key", "Consumer Secret", "Access Token", "Access Token Secret", "Status"])
	x.align["Profile Name"] = "l"
	x.align["Consumer Key"] = "l"
	x.align["Consumer Secret"] = "l"
	x.align["Access Token"] = "l"
	x.align["Access Token Secret"] = "l"
	x.align["Status"] = "l"
	x.padding_width = 1

	files = os.listdir(ppath)

	for file in sorted(files, key=lambda s: s.lower()):
		pname = file[:-8]
		with open(ppath+file, 'r') as fo:
			a = fo.readlines()
		row = [pname]
		for item in a:
			row.append(item.split(' ')[2].rstrip())
		if pname in logdeets:
			row.append(logdeets[pname])
		else:
			row.append('free')
		x.add_row(row)

	print x

def addp(filename):
        with open(filename, 'w') as fo:
                ck = raw_input("consumer_key: ")
                fo.write('consumer_key = '+ck+'\n')
                cs = raw_input("consumer_secret: ")
                fo.write('consumer_secret = '+cs+'\n')
                at = raw_input('access_token: ')
                fo.write('access_token = '+at+'\n')
                ats = raw_input('access_token_secret: ')
                fo.write('access_token_secret = '+ats+'\n')

	time.sleep(0.5)
        print 'Profile Added'
	logging.info(filename[:-8]+' added')
        return

def padd(ppath):
	print 'Adding Profile'
	logging.info('Adding profile')
	time.sleep(0.5)

	user = raw_input('Enter Twitter Username: ')

	filename = ppath+user+'.profile'

	if os.path.exists(filename):
        	ans = raw_input('Profile Already Exists. Do You Want To Overwrite? (y/n): ')
		logging.warning('Profile already exists.')
        	if ans.lower() == 'y':
                	addp(filename)
        	elif ans.lower() == 'n':
                	time.sleep(0.5)
			print 'Exiting'
			logging.info('Profile not added.')
			sys.exit()
        	else:
                	time.sleep(0.5)
			print 'Did Not Recognize Input'
			logging.error('Did not recognize input. Profile not added.')
			sys.exit()
	else:
        	addp(filename)
	return

def pdel(ppath):
	logging.info('Deleting profile')
	pname = raw_input('Enter Username: ')
	time.sleep(0.5)
	filen = ppath+pname+'.profile'

	if os.path.exists(filen):
		ans = raw_input('Confirm Deleting Profile (y): ')
		if ans.lower() == 'y':
			time.sleep(0.5)
			print 'Deleting Profile'
			os.remove(filen)
			logging.info(pname+' deleted')
		else:
			time.sleep(0.5)
			print 'Did Not Recognize Input'
			logging.warning('Did not recognize input. '+pname+' not deleted.')
	else:
		print 'Profile Does Not Exist'
		logging.warning('Profile does not exist.')

	return
