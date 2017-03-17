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
		return metch.group()
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
	global netcount
	global nettime
	global failconn
	global getafail
	global getiptime
	#print server
	iplist=[]
	try:
		netcount+=1
		time1=time.time()
		getiptime[0]+=1
		answers=dns.resolver.query(server,'A')
		for rdata in answers:
			iplist.append(rdata.address)
		time2=time.time()
		nettime+=time2-time1
		
		return iplist
	except :
		failconn+=1
		time2=time.time()
		nettime+=time2-time1
		try:
			netcount+=1
			getafail+=1
			time1=time.time()
			getiptime[1]+=1
			answers=dns.resolver.query(server,'NS')
			for rdata in answers:
				getiptime[2]+=1
				ipanswers=dns.resolver.query(rdata.target,'A')
				for rd in ipanswers:
					iplist.append(rd.address)
				netcount+=1
			time2=time.time()
			nettime+=time2-time1		
			return iplist
		except:
			failconn+=1
			#print ('can not get ip'+server)
			time2=time.time()
			nettime+=time2-time1
			return ''
def dns_resolve(domain,server):
	global nettime
	global failconn
	global netcount
	global nre
	global timelist
	try:
		q=dns.message.make_query(domain,'NS')
		q.flags=0x0000
		netcount+=1
		nre+=1
		time1=time.time()
		answers = dns.query.udp(q,server,1)
		time2=time.time()
		nettime+=time2-time1
		timelist.append((time2-time1))
		#print ('out dns_resolve')
		#print ('get ns:'+domain+server)
		return answers
	except:
		time2=time.time()
		nettime+=time2-time1
		failconn+=1
		#print ('cant get ns:'+domain+server)
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
def resolve(domain):
	#print ("target:"+domain)
	server=[]
	server.append('.')
	serverip=[]
	getnsflag=1
	nsdomain=[]
	nextserver=[]
	while len(server)!=0:
		#print ('1')
		for s in server:
			serverip=get_ip(s)
			#print ("server:"+s)
			#print serverip
			if len(serverip)==0:
				break
			ip=serverip[0]
			answers=dns_resolve(domain,ip)
			if answers:
				for rdata in answers.answer:
					for it in rdata.items:
						adddomain(find_domain(str(it)))
				for authdata in answers.authority:
					for itu in authdata.items:
						nextserver.append(find_domain(str(itu)))
						adddomain(find_domain(str(itu)))
			#print ('2')
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
	targetdomain="com.";#web1.cs.cornell.edu
	global serverqueue
	serverqueue=[]
	global result
	global nettime
	nettime=0
	global netcount
	netcount=0
	global failconn
	failconn=0
	global nre
	nre=0
	global getafail
	getafail=0
	global timelist
	global getiptime
	getiptime=[]
	timelist=[]
	result=[]
	getiptime.append(0)
	getiptime.append(0)
	getiptime.append(0)
	#print q.flags
	#q.flags=0x0000
	#answers = dns.query.udp(q,'114.114.114.114')#192.5.53.209cayuga.cs.rochester.edu
	#auth=str(answers.authority[0].items[0])
	#print find_domain(auth)
	#iplist=get_ip('.')
	#print iplist
	#dns_resolve(targetdomain,str(iplist[0]))
	totaltime1=time.time()
	adddomain(targetdomain)
	while len(serverqueue)!=0:
		tempdomain=serverqueue[0]
		del serverqueue[0]
		resolve(tempdomain)
		for node in result:
			print node
	totaltime2=time.time()
	print 'totaltime:'
	print totaltime2-totaltime1
	print 'network connect:'
	print netcount
	print 'not recursion:'
	print nre
	print 'fail conn:'
	print failconn
	print 'network time'
	print nettime
	print 'first connect failed count:'
	print getafail
	timelist.sort()
	print 'timemax:'
	print timelist[len(timelist)-1]
	print 'timemin:'
	print timelist[0]
	print 'timemid:'
	print timelist[len(timelist)/2]
	print 'timeaverage:'
	sumt=0
	for t in timelist:
		sumt+=t
	print sumt/len(timelist)
	print getiptime
