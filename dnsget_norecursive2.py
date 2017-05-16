#coding=utf-8
import dns.resolver
import re
import time
import json
import csv
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
		return ''#ipv6 return ''
def ns_query(domain,serverip):
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
def is_done(domain):
	global localcache
	global gcache
	ip=localcache.get(domain,0)
	if ip!=0:
		#print 'in done'
		#print ip
		return ip
	else :
		ip=gcache.get(domain,0)
		if ip!=0:
			return ip
		else:
			return 0
def addlog(domain,serverip,servername,time):
	#error num:
	#0 同一级权威服务器，给出答案中的域不同
	#1-3 访问超时1-3次
	global logfile
	temp=[]
	temp.append(domain)
	temp.append(serverip)
	temp.append(servername)
	temp.append(time)
	outlog=open("./log/"+logfile+".json",'a')
	json_dependency=json.dumps(temp)
	outlog.write(json_dependency)
	outlog.close()	
def addresult(ip,query,ans):
	global result
	temp={}
	temp['sip']=ip
	temp['q']=query
	temp['ans']=[]
	for rdata in ans.answer:
		temp['ans'].append(str(rdata))
	
	temp['aut']=[]
	temp['autname']=''
	for au in ans.authority:
		temp['autname']=find_domain(str(au.name))
		for at in au.items:
			temp['aut'].append(str(at))
		
	temp['add']=[]
	for ad in ans.additional:
		temp['add'].append(str(ad))
	result.append(temp)

def a_query(domain,serverip,servername):
	iplist=[]
	if serverip=='':
		return ''
	t=0
	#print 'Q:'+domain+serverip
	try:
		q=dns.message.make_query(domain,'A')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		addresult(serverip,domain,answers)
		return answers
	except :
		t+=1
		try:
			q=dns.message.make_query(domain,'A')
			q.flags=0x0000
			answers = dns.query.udp(q,serverip,1)
			addresult(serverip,domain,answers)
			addlog(domain,serverip,servername,t)
			return answers
		except:
			t+=1
			try:
				q=dns.message.make_query(domain,'A')
				q.flags=0x0000
				answers = dns.query.udp(q,serverip,1)
				addresult(serverip,domain,answers)
				addlog(domain,serverip,servername,t)
				return answers
			except :
				t+=1
				addlog(domain,serverip,servername,t)
				#print e.message
				#print 'noanswer'
				return ''
def ns_query(domain,serverip,servername):
	t=0
	try:
		q=dns.message.make_query(domain,'NS')
		q.flags=0x0000
		answers = dns.query.udp(q,serverip,1)
		addresult(serverip,domain,answers)
		return answers
	except:
		t+=1
		addlog(domain,serverip,servername,t)
		return ''
def adds2l(ip,newip):
	flag=0
	if newip=='':
		return ip
	else:
		for i in ip:
			if newip==i:
				return ip
		ip.append(newip)
		return ip
def newserver(server,server2):
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
			newserver.append(s2)
	return newserver
def addl2l(ip,newip):

	for ni in newip:
		flag=0
		for i in ip:
			if ni==i:
				flag=1
				break
		if flag==0:
			ip.append(ni)
	return ip
def addlocalcache(domain,ip):
	global localcache
	#print cache
	if localcache.has_key(domain):
		localcache[domain]=addl2l(localcache[domain],ip)
	else :
		localcache.setdefault(domain,ip)
def resolver(domain,ceng):
	global rootip
	global ing
	ceng+=1
	#print ceng
	#print domain
	ip=[]
	server={}
	server['domain']='.'
	server['ip']=[]
	server['name']=[]
	ans=a_query(domain,rootip[11],server['domain'])
	if ans!='':
		findip=0
		for a in ans.additional:
			if (str(a.name)).lower()==domain:
				ip=adds2l(ip,find_ip(str(a.items)))
				findip=1
		if findip==1 :
			#print 'ip find:'
			#print domain
			#print 'from root'
			addlocalcache(domain,ip)
			return ip
		else :

			for a1 in ans.authority:
				server['domain']=find_domain(str(a1.name))
			gtlddomain=server['domain']
			nsans=ns_query(gtlddomain,rootip[11],'.')
			if nsans!='':
				for a in nsans.additional:
					server['ip'].append(find_ip(str(a.items)))
					server['name'].append(find_domain(str(a.name)))
					gtldip=[]
					gtldip.append(find_ip(str(a.items)))
					addlocalcache(find_domain(str(a.name)),gtldip)
			else :
				for a in ans.additional:
					server['ip'].append(find_ip(str(a.items)))
					server['name'].append(find_domain(str(a.name)))
					gtldip=[]
					gtldip.append(find_ip(str(a.items)))
					addlocalcache(find_domain(str(a.name)),gtldip)
		while len(server['ip'])>0:
			server2=[]
			server2name=[]
			server2domain=''
			noserver2name=[]
			for si in server['ip']:
				findip=0
				ans2=a_query(domain,si,server['domain'])
				if ans2!='':
					for rdata in ans2.answer:
						if rdata.rdtype==1:
							for it in rdata.items:
								ip=adds2l(ip,find_ip(str(it)))
								findip=1
						elif rdata.rdtype==5:
							tdflag=0
							for it in rdata.items:
								tempdomain=find_domain(str(it))
								for i in ing:
									if i==tempdomain:
										tdflag=1
										break
								if tdflag==1:
									continue
								ing.append(tempdomain)
								ipdone=is_done(tempdomain)
								if ipdone!=0:
									ip=addl2l(ip,ipdone)
								else:
									tempip=resolver(tempdomain,ceng)
									ip=addl2l(ip,tempip)
								del ing[-1]
								findip=1
					if findip==1:
						#print 'ip find(ans):'
						#print domain
						#print server
						continue
						#pass
					#for a in ans2.additional:
					#	if (str(a.name)).lower()==domain:
					#		ip=adds2l(ip,find_ip(str(a.items)))
					#		findip=1
					#if findip==1 :
						#print 'ip find(aut):'
						#print domain
						#print server
					#	continue
					
					for a in ans2.additional:
						if (find_domain(str(a.name)).lower()).endswith(str(server['domain'])):
							server2=adds2l(server2,find_ip(str(a.items)))
							noserver2name=adds2l(noserver2name,find_domain(str(a.name)))
							addip=[]
							addip.append(find_ip(str(a.items)))
							#addcache(find_domain(str(a.name)),addip)
					for a2 in ans2.authority:
						server2domain=find_domain(str(a2.name))
						for a2i in a2.items:
							fadd=0
							for n2n in noserver2name:
								if str(a2i)==n2n:
									fadd=1
									break
							if fadd==0:
								server2name=adds2l(server2name,find_domain(str(a2i)))
			for	s2n in server2name:
				tdflag=0
				for i in ing:
					if i==s2n:
						tdflag=1
						break
				if tdflag==1:
					continue
				ing.append(s2n)
				ipdone=is_done(s2n)
				if ipdone!=0:
					server2=addl2l(server2,ipdone)
				else:
					iptemp=resolver(s2n,ceng)
					server2=addl2l(server2,iptemp)
				del ing[-1]
			server['ip']=newserver(server['ip'],server2)
			server['name']=newserver(server['name'],server2name)
			server['domain']=server2domain
	addlocalcache(domain,ip)
	#debug
	return ip
def init(target):
	global rootip
	global logfile
	rootip=['198.41.0.4', '192.228.79.201', '192.33.4.12', '199.7.91.13', '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42', '202.12.27.33']
	outlog=open("./log/"+logfile+".json",'a')
	#t=time.strftime("%Y-%m-%d-%H:%M:%S",time.localtime())
	outlog.write(target+'\n')
	outlog.close()
def recursive(domain):
	iplist=[]
	try:
		answers=dns.resolver.query(domain,'A')
		for rdata in answers:
			iplist.append(rdata.address)
		return iplist
	except:
		#print 'can not get ip'+domain
		return iplist	
def refreshcache():
	global localcache
	global gcache
	if len(gcache)<100000:
		gcache=dict(gcache,**localcache)
	else:
		return
def dnsget(target,filename,log):
	global localcache
	global ing
	global filename2
	global result
	global logfile
	localcache={}
	logfile=log
	filename2=filename
	result=[]
	ing=[]
	init(target)
	if target[-1]!='.':
		target=target+'.'
	target=target.lower()
	ip=recursive(target)
	if len(ip)>0:
		ing.append(target)
		ipres=resolver(target,0)
		if len(ipres)==0:
			print target+'failed'
	else :
		print target+' cannt conn'
	refreshcache()
	output=open("./resultnr/"+filename2+".json",'a')
	json_dependency=json.dumps(result)
	output.write(target+'\n')
	output.write(json_dependency)
	output.write('\n')
	output.close()
if __name__=='__main__':
	global gcache
	gcache={}
	f=open("top-1m.csv","rb")
	reader=csv.reader(f)
	i=0
	for row in reader:
		i+=1
		t1=time.time()
		name=row[1]
		print i
		print name
		dnsget(name,'5-16-2','5-16-2')
		t2=time.time()-t1
		print t2
	f.close()
