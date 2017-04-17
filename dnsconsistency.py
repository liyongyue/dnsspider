import dns.resolver
import re
import time
class node:
	def __init__(self,nodeid,domain,childid):
		self.domain=domain
		self.nodeid=nodeid
		self.children=[]
		self.children.append(childid)
	def addchild(self,childid):
		self.children.append(childid)
def find_domain(string):
	domain_re=re.compile(r'(\S*?\.)+')
	metch=domain_re.search(string)
	if metch:
		return metch.group().lower()
	else:
		return ''
def find_ip(string):
	ip_re=re.compile(r'(\d{1,3}\.){3}(\d{1,3})')
	metch=ip_re.search(string)
	if metch:
		return metch.group()
	else:
		return ''
def get_ip(server):
	global ipcache
	#print server
	ip=ipcache.get(server,0)
	if ip==0:
		iplist=[]
		try:
			answers=dns.resolver.query(server,'A')
			for rdata in answers:
				iplist.append(rdata.address)
			return iplist
		except:
			#print ('NS no answer')
			try:
				answers=dns.resolver.query(server,'NS')
				for rdata in answers:
					ipanswers=dns.resolver.query(rdata.target,'A')
					for rd in ipanswers:
						iplist.append(rd.address)
				ipcache.setdefault(server,iplist)
				return iplist
			except:
				#print 'queryerror'
				return ''
	else :
		return ip
def dns_resolve(domain,serverip):
	#print (domain+serverip)
	try:
		q=dns.message.make_query(domain,'MX')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		#print ('out dns_resolve')
		
		return answers
	except:
		#print ('get ns from target server error')
		return ''
	#for rdata in answers.authority:
		#domainlist.append(rdata.answer)
	#	print rdata.items
	#return domainlist
def addresult(domain):
	global result
	result.append(domain)
def adddomain(domain):
	global serverqueue
	global result
	flag=0
	#frag=domain.split('.')
	#for i in range(1,len(frag)):
	#	tempdomain=''
	#	flag=0
	#	for j in range(i,len(frag)):
	#		tempdomain=tempdomain+frag[j]+'.'
	#	for k in range(0,len(serverqueue)):
			#print serverqueue[k]
	#		if serverqueue[k]==tempdomain:
	#			flag=1
	#			break
	for m in result:
		if m==domain:
			flag=1
			break
	if flag==0:
		for n in serverqueue:
			if n==domain:
				flag=1
				break
	if flag==0:
		serverqueue.append(domain)
		addresult(domain)
def compdo(fip,first,last,que):
	global test
	flag=0
	for l in last:
		flag=0
		for f in first:
			if l==f:
				flag=1
				break
		if flag==0:
			test.append(fip+l+que)
def resolve(domain):
	#print ("target:"+domain)
	server=[]
	server.append('.')
	serverip=[]
	getnsflag=1
	nsdomain=[]
	fipns=[]
	nextserver=[]
	while len(server)!=0:
		#print ('1') 
		for s in server:
			k=0
			del fipns[:]
			del nsdomain[:]
			serverip=get_ip(s)
			#print ("server:"+s)
			#print serverip
			if len(serverip)==1:
				for ii in range(1,5):
					serverip.append(serverip[0])
			for ip in serverip:
				del nsdomain[:]
				answers=dns_resolve(domain,ip)
				if answers:
					for rdata in answers.answer:
						for it in rdata.items:
							if k==0:
								fip=ip
								fipns.append(find_domain(str(it)))
							else:
								nsdomain.append(find_domain(str(it)))
							adddomain(find_domain(str(it)))
					for authdata in answers.authority:
						for itu in authdata.items:
							if k==0:
								fip=ip
								fipns.append(find_domain(str(itu)))
							else:
								nsdomain.append(find_domain(str(itu)))
							nextserver.append(find_domain(str(itu)))
							adddomain(find_domain(str(itu)))
			#print ('2')				if k==1:
					compdo(fip,fipns,nsdomain,ip+domain)
					k=1
		i=0
		while i<len(nextserver):
			flag=0
			for se in server:
				if se==nextserver[i]:
					del nextserver[i]
					flag=1
					break
			if flag==0:
				i+=1
		del server[:]
		for nd in nextserver:
			flag=0
			for se in server:
				if se==nd:
					flag=1
			if flag==0:
				server.append(nd)
		del nextserver[:]
		#print ('3')
if __name__ == '__main__':
	global serverqueue
	serverqueue=[]
	global result
	global test
	global ipcache
	ipcache={}
	test=[]
	result=[]
	#print q.flags
	#q.flags=0x0000
	#answers = dns.query.udp(q,'114.114.114.114')#192.5.53.209cayuga.cs.rochester.edu
	#auth=str(answers.authority[0].items[0])
	#print find_domain(auth)
	#iplist=get_ip('.')
	#print iplist
	#dns_resolve(targetdomain,str(iplist[0]))
	time1=time.time()
	adddomain('sina.com.cn.')
	adddomain('weibo.com.')
	adddomain('wikipedia.org.')
	while len(serverqueue)!=0:
		tempdomain=serverqueue[0]
		del serverqueue[0]
		resolve(tempdomain)
	time2=time.time()
	for t in test:
		print t
	print len(test)
	print time2-time1
