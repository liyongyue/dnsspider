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
def ns_query(domain,serverip):
	global rootserver
	auth=[]
	try:
		q=dns.message.make_query(domain,'NS')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		for authdata in answers.authority:
			for itu in authdata.items:
				auth.append(find_domain(str(itu)))
		return auth
	except:
		return auth
def a_query(domain.serverip):
	global rootserver
	iplist=[]
	try:
		q=dns.message.make_query(domain,'A')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		for rdata in answers:
			iplist.append(rdata.address)
		return iplist
	except:
		return iplist
def resolver(domain):
	global rootip
	ans=a_query(domain,rootip[0])
def init():
	global rootserver
	global rootip
	rootserver.append('a.root-servers.net.')
	rootserver.append('b.root-servers.net.')
	rootserver.append('c.root-servers.net.')
	rootserver.append('d.root-servers.net.')
	rootserver.append('e.root-servers.net.')
	rootserver.append('f.root-servers.net.')
	rootserver.append('g.root-servers.net.')
	rootserver.append('h.root-servers.net.')
	rootserver.append('i.root-servers.net.')
	rootserver.append('j.root-servers.net.')
	rootserver.append('k.root-servers.net.')
	rootserver.append('l.root-servers.net.')
	rootserver.append('m.root-servers.net.')
	for r in rootserver:
		try:
			answers=dns.resolver.query(r,'A')
			for rdata in answers:
				rootip.append(rdata.address)
		except:
			continue
def nrecursive(t,filename):
	global serverqueue
	serverqueue=[]
	global done
	global ipcache
	global result
	global rootserver
	global rootip
	rootip=[]
	rootserver=[]
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
