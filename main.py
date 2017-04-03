from dnsget import dnsget
from analyse_dependency import a_d
f=open("targetd2r")
line=f.readline().strip('\n')
target=[]
while (line):
	target=[]
	target.append(line)
	#name=time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime())
	name=str(line)
	r=dnsget(target,name)
	print r
	a_d(name)
	line=f.readline().strip('\n')
f.close()

