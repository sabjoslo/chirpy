import sys

input_file = sys.argv[1]
f = open(input_file, 'r').read()

for line in f:
	print f
