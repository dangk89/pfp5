with open('data/links-simple-sorted.txt') as infile:
	pages = [[int(num) for num in e.replace(':','').split(' ')] for e in infile.read().split('\n')]


fromTo 			= [(e[0],out) for e in pages for out in e[1:]]
frm, to, deg 	= [e[0] for e in fromTo],[e[1] for e in fromTo],[len(e)-1 for e in pages]


