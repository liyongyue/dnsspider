from dnsget import dnsget
from analyse_dependency import a_d
f=open("targetd2")
line=f.readline().strip('\n')
o=open("targetd2r",'w')
target=[]
name="top50"
while (line):
	target.append(line)
	line=f.readline().strip('\n')
r=dnsget(target,name)
a_d(name)
f.close()
o.close()
