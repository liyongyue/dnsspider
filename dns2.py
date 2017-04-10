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
	global ipcache
	print server
	ip=ipcache.get(server,0)
	if ip==0:
		iplist=[]
		try:
			answers=dns.resolver.query(server,'A')
			for rdata in answers:
				iplist.append(rdata.address)
			ipcache.setdefault(server,iplist)
			return iplist
		except:
			print ('NS no answer')
			try:
				answers=dns.resolver.query(server,'NS')
				for rdata in answers:
					ipanswers=dns.resolver.query(rdata.target,'A')
					for rd in ipanswers:
						iplist.append(rd.address)
				ipcache.setdefault(server,iplist)
				return iplist
			except:
				print 'queryerror'
				return ''
	else :
		return ip
def dns_resolve(domain,serverip):
	global result
	temp={}
	print (domain+serverip)
	auth=[]
	ans=[]
	try:
		q=dns.message.make_query(domain,'NS')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		#print ('out dns_resolve')
		for authdata in answers.authority:
			for itu in authdata.items:
				auth.append(find_domain(str(itu)))
		for rdata in answers.answer:
			for it in rdata.items:
				ans.append(find_domain(str(it)))
		temp['question']=find_domain(str(answers.question))
		temp['flags']=answers.flags
		temp['answer']=ans
		temp['authority']=auth
		result.append(temp)
		return answers
	except:
		print ('get ns from target server error')
		return ''
def adddone(domain):
	global done
	done.append(domain)
def adddomain(domain):
	global serverqueue
	global done
	flag=0
	for m in done:
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
def resolve(domain):
	print ("target:"+domain)
	server=[]
	server.append('.')
	serverip=[]
	getnsflag=1
	nsdomain=[]
	nextserver=[]
	while len(server)!=0:
		for s in server:
			del nsdomain[:]
			serverip=get_ip(s)
			print ("server:"+s)
			print serverip
			for ip in serverip:
				del nsdomain[:]
				answers=dns_resolve(domain,ip)
				adddone(domain)
				if answers:
					for rdata in answers.answer:
						for it in rdata.items:
							adddomain(find_domain(str(it)))
					for authdata in answers.authority:
						for itu in authdata.items:
							nextserver.append(find_domain(str(itu)))
							adddomain(find_domain(str(itu)))
					break
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
if __name__ == '__main__':
	targetdomain="com"
	global serverqueue
	serverqueue=[]
	global done
	global ipcache
	global result
	result=[]
	ipcache={}
	test=[]
	done=[]
	time1=time.time()
	adddomain('com')
	while len(serverqueue)!=0:
		tempdomain=serverqueue[0]
		del serverqueue[0]
		resolve(tempdomain)
	print result
	time2=time.time()
	print time2-time1
