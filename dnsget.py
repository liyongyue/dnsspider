#coding=utf-8
import dns.resolver
import re
import time
import json
def find_domain(string):
	domain_re=re.compile(r'(\S*?\.)+')
	metch=domain_re.search(string)
	if metch:
		return metch.group()
	else:
		return ''
def resolve(domain,index):
	global dqueue
	global result
	global log
	ns=[]
	try :
		answers=dns.resolver.query(domain,'NS')
		for rdata in answers.rrset:
			ad=str(rdata).lower()
			flag=0
			for d in dqueue:
				if d==ad:
					flag=1
					break
			if flag==0:
				dqueue.append(ad)
			ns.append(ad)
		temp=[]
		temp.append(domain)
		temp.append(index)
		temp.append(ns)
		result.append(temp)
		#print '+'+domain
	except:
		#print domain
		log.write("can not get ns "+domain)
		#print '-'+domain
		temp=[]
		temp.append(domain)
		temp.append(index)
		temp.append(ns)
		result.append(temp)
def separate(domain,index):
	global result
	frag=domain.split('.')
	for i in range(0,len(frag)-1):
		f=0
		f2=0
		temp=''
		for j in range(i,len(frag)-1):
			temp=temp+frag[j]+'.'
		for r in result:
			if r[0]==temp:
				f=1
				break
			for ns in r[2]:
				if ns==temp:#此域名为一个权威服务器
					f2=1
					break
		if f2==1:
			continue
		if f==0 and f2==0:
			resolve(temp,index)
			#print temp
		if f==1:
			break
class dependency():
	def __init__(self,d,index,n):
		self.domain=d
		self.id=index
		self.ns=n
def dnsget(t,filename):#t is a list
	global dqueue
	dqueue=[]
	global result
	global log
	result=[]
	j=[]
	i=0
	log=open("./log/"+filename+".log",'w')
	for target in t:
		if target[-1]!='.':
			target=target+'.'
		dqueue.append(target.lower())
		while len(dqueue)!=0:
			tempd=dqueue[0]
			del dqueue[0]
			separate(tempd,i)
		i+=1	
	#print dqueue
	output=open("./result/"+filename+".json",'w')
	for r in result:
		d=dependency(r[0],r[1],r[2])
		j.append(d.__dict__)
	json_dependency=json.dumps(j)
	output.write(json_dependency)
	output.close()
	log.close()
	return len(result)
