import dns.resolver
import re
import time
import json
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
			print 'can not get ip'+server
			return iplist
	else :
		return ip
def dns_resolve(domain,serverip,server):
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
			auth.append(str(authdata.name))
			for itu in authdata.items:
				auth.append(find_domain(str(itu)))
		for rdata in answers.answer:
			for it in rdata.items:
				ans.append(find_domain(str(it)))
		temp['question']=find_domain(str(answers.question))
		temp['server']=server
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
	server.append('a.root-servers.net.')
	server.append('b.root-servers.net.')
	server.append('c.root-servers.net.')
	server.append('d.root-servers.net.')
	server.append('e.root-servers.net.')
	server.append('f.root-servers.net.')
	server.append('g.root-servers.net.')
	server.append('h.root-servers.net.')
	server.append('i.root-servers.net.')
	server.append('j.root-servers.net.')
	server.append('k.root-servers.net.')
	server.append('l.root-servers.net.')
	server.append('m.root-servers.net.')
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
				answers=dns_resolve(domain,ip,s)
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
def nrecursive(t,filename):
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
	for target in t:
		if target[-1]!='.':
			target=target+'.'
		serverqueue.append(target.lower())
		while len(serverqueue)!=0:
			tempdomain=serverqueue[0]
			del serverqueue[0]
			resolve(tempdomain)
	output=open("./resultnr/"+filename+".json",'w')
	json_dependency=json.dumps(result)
	output.write(json_dependency)
	output.close()
	print result
	time2=time.time()
	print time2-time1
