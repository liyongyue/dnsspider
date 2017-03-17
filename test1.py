def func(ww):
	b=[]
	b.append(ww)
	b.append(ww)
	return b
a=[]
a.append('a')
a.append('b')
a.append('c')
print a
del a[1]
print a[1]
print len(a)
for q in range(0,len(a)):
	print a[q]
for w in a:
	print w
c=func('q')
print c
c=func('w')
print c
