import dns.resolver
domain='cn.'
try :
	q=dns.message.make_query(domain,'A')
	q.flags=0x0000
	answers = dns.query.udp(q,'198.41.0.4',1)
	for a in answers.additional:
		print a.name
		print a.items
except:
	print '--'
