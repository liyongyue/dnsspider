import dns.resolver
import re
def get_ip(server):
	print server
	iplist=[]
	try:
		answers=dns.resolver.query(server,'NS')
		print answers
		for rdata in answers:
			ipanswers=dns.resolver.query(rdata.target,'A')
			for rd in ipanswers:
				iplist.append(rd.address)
		return iplist
	except dns.resolver.NoAnswer:
		print ('NS no answer')
		try:
			answers=dns.resolver.query(server,'A')
			for rdata in answers:
				print rdata
				iplist.append(rdata.address)
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
domain='cs.cornell.edu'
server=get_ip('dns.cit.cornell.edu')
print server
try:
	q=dns.message.make_query(domain,'A')
	domainlist=[]
	q.flags=0x0000
	answers = dns.query.udp(q,server[0],5)
	print answers
	for authdata in answers.authority:
		print authdata.items[0]
except:
	print ('get ns from target server error')
