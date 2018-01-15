import json
import numpy as np 

def parse(file):
	pages = [[int(num) for num in e.replace(':','').split(' ') if num] for e in file]
	frmTo 		= [(e[0],out) for e in pages for out in e[1:]]
	frm,to,deg 	= [e[0] for e in frmTo],[e[1] for e in frmTo],[len(e)-1 for e in pages]

	with open('data/from.txt', 'a') as outfile:
		json.dump(frm, outfile)
	with open('data/to.txt', 'a') as outfile:
		json.dump(to, outfile)
	with open('data/deg.txt', 'a') as outfile:
		json.dump(deg, outfile)

bigfile = open('data/links-simple-sorted.txt','r')
tmp_lines = bigfile.readlines(10)
for i in range(2):
	parse(tmp_lines)
    	tmp_lines = bigfile.readlines(10)


"""# METHOD 1
with open('data/links-simple-sorted.txt') as infile:
	lines = []
	for each in range(0,5000000):
		line = infile.readline()
		page = [int(num) for num in line.replace(':','').split(' ') if num]
		frm,to,deg= page[0],page[1:],len(page)-1
		with open('data/from.txt', 'w') as outfile:
			json.dump(frm, outfile)
		with open('data/to.txt', 'w') as outfile:
			json.dump(to, outfile)
		with open('data/deg.txt', 'w') as outfile:
			json.dump(deg, outfile)"""


# METHOD 2
#with open('data/links-simple-sorted.txt') as infile:
#	pages = [[int(num) for num in e.replace(':','').split(' ') if num] for e in infile.read().split('\n')]

#print(len(pages))

"""
fromTo 		= [(e[0],out) for e in pages for out in e[1:]]
frm,To,Deg 	= [e[0] for e in fromTo],[e[1] for e in fromTo],[len(e)-1 for e in pages]

with open('output.txt', 'w') as outfile:
    json.dump(frm, outfile)
    outfile.write('\n')
    json.dump(To, outfile)
    outfile.write('\n')
    json.dump(Deg, outfile)
"""


# 5706071 lineszz