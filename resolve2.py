import dns.resolver
domain='.'
try :
	answers=dns.resolver.query(domain,'A')
	for rdata in answers.rrset:
		print rdata
except:
	print '--'
