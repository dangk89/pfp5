with open('titles.txt') as infile:
	titles = infile.read().split('\n')

with open('pages.txt') as infile:
	pages = [e.replace(':','').split(' ') for e in infile.read().split('\n')[:-1]]

print(pages)

a = [1,2,3]
del a