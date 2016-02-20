import sys
import numpy as np
import time

input_file = sys.argv[1]
f = open(input_file, 'a')

while True:
	userid = str(np.random.random_integers(0,high=9))
	for i in range(4):
		userid = userid + str(np.random.random_integers(0,high=9))
	f.write(userid + '\n')
	print userid
	time.sleep(6)


