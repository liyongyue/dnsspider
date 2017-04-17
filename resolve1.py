import dns.resolver
import re
import time
def get_ip(server):
	print server
	iplist=[]
	try:	
		answers=dns.resolver.query(server,'A')
		for rdata in answers:
			#print rdata
			iplist.append(rdata.address)
		return iplist
	except :
		print ('A no answer')
		try:
			answers=dns.resolver.query(server,'NS')
			#print answers
			for rdata in answers:
				ipanswers=dns.resolver.query(rdata.target,'A')
				for rd in ipanswers:
					iplist.append(rd.address)
			return iplist
		except:
			print 'queryerror'
			return ''
def find_domain(string):
	domain_re=re.compile(r'(\S*?\.)+')
	metch=domain_re.search(string)
	if metch:
		return metch.group()
	else:
		return ''
count={}
for i in range(1):
	domain='net.'
	server=get_ip('.')
	#print server
	try:
		q=dns.message.make_query(domain,'A')
		domainlist=[]
		q.flags=0x0000
		answers = dns.query.udp(q,server[0],1)
		print answers
	#print answers.question
	#print answers.answer
		k=0
		for authdata in answers.authority:
			for itu in authdata.items:
				#print itu
				k+=1
		if count.has_key(k):
			m=count[k]
			m+=1
			count[k]=m
		else :
			count[k]=1
	#print ' '
	#for authdata in answers.authority:
	#	print authdata.items[0]
	except:
		print ('get ns from target server error')
	time.sleep(0.5)
print count
