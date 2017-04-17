from dnsget_norecursive import nrecursive
from analyse_norecursive import analyse_nr
f=open("targetd2r")
line=f.readline().strip('\n')
target=[]
while (line):
	target=[]
	target.append(line)
	#name=time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime())
	name=str(line)
	#nrecursive(target,name)
	analyse_nr(name)
	line=f.readline().strip('\n')
f.close()

