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
bufsize = 1000000

# Create output files
path = 'data/frmtodeg/'
fromfile = open(path+'/from'+str(n_chunk)+'.txt','a')
tofile = open(path+'/to'+str(n_chunk)+'.txt','a')
degfile = open(path+'/deg'+str(n_chunk)+'.txt','a')
infile = open('data/links-simple-sorted.txt')
frmv = []
tov = []
degv = []
for line in infile:
		line = [int(num) for num in line.replace(':','').split(' ') if num]
		frmTo = [(line[0],out) for out in line[1:]]
		frm,to,deg = [e[0] for e in frmTo],[e[1] for e in frmTo],len(line[1:])

		if n_line%100000 == 0:
			print(n_line)
		n_line+=1

		for idx,e in enumerate(frm):
			frmv.append(e)
			tov.append(to[idx])
			degv.append(deg)

			n_links+=1
			if n_links%bufsize == 0:
				fromfile.write('['+','.join([str(e) for e in frmv])+']')
				tofile.write('['+','.join([str(e) for e in tov])+']')
				degfile.write('['+','.join([str(e) for e in degv])+']')
				n_chunk+=1
				fromfile = open(path+'/from'+str(n_chunk)+'.txt','a')
				tofile = open(path+'/to'+str(n_chunk)+'.txt','a')
				frmv = []
				tov = []
				degv = []

		if n_line>10000:
			break

fromfile.write('['+','.join([str(e) for e in frmv])+']')
tofile.write('['+','.join([str(e) for e in tov])+']')
degfile.write('['+','.join([str(e) for e in degv])+']')

n_chunk+=1
#fromfile = open(path+'/from'+str(n_chunk)+'.txt','a')
#tofile = open(path+'/to'+str(n_chunk)+'.txt','a')
#degfile = open(path+'/deg'+str(n_chunk)+'.txt','a')

#frmv = []
#tov = []