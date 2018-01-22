import json
import numpy as np
import os
import sys

#Clear outfiles
for file in os.listdir('data/frmtodeg'):
	os.remove('data/frmtodeg/'+file)

# Initial configs
n_line = 0
n_chunk = 0
n_links = 0
bufsize = 10**6

# Create output files
path = 'data/frmtodeg/'
infile = open('data/links-simple-sorted.txt')
degrees_file = open(path+'/degrees.txt','a')
links_file = open(path+'/links.txt','a')

links_vector = []
degrees_vector = []

def write_to_disk():
	links_file.write('['+','.join("[{},{}]".format(e[0], e[1]) for e in links_vector)+']')
	degrees_file.write('['+','.join([str(e) for e in degrees_vector])+']')

for line in infile:
	line = [int(num) for num in line.replace(':','').split(' ') if num]
	links = [(line[0], out) for out in line[1:]]
	length = len(line[1:])
	links_vector += links
	degrees_vector.append(length)

	n_line += 1
	n_links += length
	if (n_chunk + 1) * bufsize < n_links:
		print("Writing {} links to disk".format(n_links))
		write_to_disk()
		n_chunk += 1
		links_vector = []
		degrees_vector = []

# Write residual to files
write_to_disk()

print("Wrote {} chunks with {} links and {} pages to disk".format(n_chunk, n_links, n_line))
