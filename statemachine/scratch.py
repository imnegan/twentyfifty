a=set()
l=['a', 'b','c']
tl=tuple(l)
sl=set(l)
d={'a':'a', 'b':'b', 'c':'c'}
fd=frozenset(d)
a.add(fd)
a.add(tl)

bd={'a':True, 'b':True, 'c':False}
print(bd)

for key in bd.keys():
	print(key)
