import dns.resolver
domain='h.gtld-servers.net.'
try :
	answers=dns.resolver.query(domain,'NS')
	for rdata in answers.rrset:
		print rdata
except:
	print '--'
