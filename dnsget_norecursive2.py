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
	ans={}
	try:
		q=dns.message.make_query(domain,'NS')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		
		for authdata in answers.authority:
			ans['name']=str(authdata.name)
			ans['authority']=[]
			for itu in authdata.items:
				ans['authority'].append(find_domain(str(itu)))
		return ans
	except:
		return ans
def a_query(domain,serverip):
	global rootserver
	iplist=[]
	try:
		q=dns.message.make_query(domain,'A')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		return answers
	except:
		return ''
def dns_query(domain,serverip):
	try:
		q=dns.message.make_query(domain,'A')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		return answers
	except:
		return ''
def addip(ip,newip):
	flag=0
	for i in ip:
		if newip==i:
			return ip
	ip.append(newip)
	return ip
def addserver(server,server2):
	newserver=[]
	for s2 in server2:
		flag=0
		for s in server:
			if s2==s:
				flag=1
				break
		for ns in newserver:
			if s2==ns:
				flag=1
				break
		if flag==0:
			newserver.append(ns)
	return newserver
def resolver(domain):
	global rootip
	ans=a_query(domain,rootip[0])
	serverip=[]
	ip=[]
	server=[]
	server2=[]
	if ans!='':
		flag=0
		for a in ans.additional:
			if a.name==domain:
				ip.extend(find_ip(str(a.items)))
				flag=1
		if flag==1 :
			return ip
		else :
			for a in ans.authority:
				server.append(find_domain(str(a.items)))
			while len(server)>0:
				for s in server:					
					serverip.extend(resolver(s))
				for si in serverip:
					findip=0
					ans2=a_query(domain,si)
					if ans2!='':
						for rdata in ans2.answer:
							for it in rdata.items:
								ip=addip(ip,find_ip(str(it)))
								findip=1
						if findip==1:
							continue
						for a in ans2.authority:
							server2.append(find_domain(str(a.items)))
				server=addserver(server,server2)
	return ip
def init():
	global rootserver
	rootserver=[]
	global rootip
	rootip=[]
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
def recursive(domain):
	iplist=[]
	try:
		answers=dns.resolver.query(domain,'A')
		for rdata in answers:
			iplist.append(rdata.address)
		return iplist
	except:
		print 'can not get ip'+domain
		return iplist	
if __name__=='__main__':
	init()
	time1=time.time()
	target='www.baidu.com'
	ip=recursive(target)
	if len(ip)>0:
		print ip
		print resolver(target)
	time2=time.time()
	print time2-time1
