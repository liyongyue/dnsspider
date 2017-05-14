import json
import re
import networkx as nx
import matplotlib.pyplot as plt
import dns.resolver
def readjson(filename):
	with open(filename,'r') as f:
		data=json.load(f)
	return data
def addnode(nodes,domain):
	if domain!='':
		for n in nodes:
			if n==domain:
				return
		nodes.append(domain)
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
def find_cname(string):
	frag=string.split(' ')
	for f in range(0,len(frag)):
		domain=find_domain(frag[f])
		if domain!='':
			for i in range(f+1,len(frag)):
				ip=find_ip(frag[i])
				if ip!='':
					return ''
				cname=find_domain(frag[i])
				if cname!='':
					return cname
	return ''
	#cname_re=re.compile(r'((\S*?\.)+)([\s\S]*)(CNAME)(\s)((\S*?\.)+)')
		
def addedge(nodes,edges,start,end,d,method):
	f1=False
	f2=False
	for i in range(0,len(nodes)):
		if nodes[i]==start:
			f1=True
			break
	for j in range(0,len(nodes)):
		if nodes[j]==end:
			f2=True
			break
	if edges[i][j]==9999:
		print '9999:'
		print d
		print method
		print start
		print end
	if f1 and f2:
		edges[i][j]=1
	else:
		print 'not find node ERROR!'
		print start
		print end
		print d
		print method
class nodepos():
	def __init__(self,domain,index,x,y):
		self.domain=domain
		self.id=index
		self.x=x
		self.y=y
class depedge():
	def __init__(self,node1,node2):
		self.source=node1
		self.target=node2
class map():
	def __init__(self,nodes,links):
		self.nodes=nodes
		self.links=links

def draw_graph(nodes,edges,nodeid):
	G=nx.DiGraph()
	for n in nodes:
		G.add_node(n)
	for i in range(0,len(edges)):
		for j in range(0,len(edges)):
			if edges[i][j]==1:
				G.add_edge(nodes[i],nodes[j])
	pos = nx.spring_layout(G)
	nx.draw(G,pos,node_size=10000,node_color='w')
	i=0
	js=[]
	jse=[]
	for p in pos:
		plt.text(pos.values()[i][0],pos.values()[i][1],pos.keys()[i],horizontalalignment='center')
		p=nodepos(nodes[i],nodeid[i],pos.values()[i][0]*200,pos.values()[i][1]*200)
		js.append(p.__dict__)
		i+=1
	json_np=json.dumps(js)
	for i in range(0,len(edges)):
		for j in range(0,len(edges)):
			if edges[i][j]==1 and i!=j:
				d=depedge(i,j)
				jse.append(d.__dict__)
	m=map(js,jse)
	print len(js)
	print len(jse)
	json_m=json.dumps(m.__dict__)
	output=open('./map/position.json','w')
	output.write(json_m)
	output.close()
	plt.show()
def find_edge(nodes,edges):
	for n in range(0,len(nodes)):
		if nodes[n]=='cuhk.edu.hk.':
			break
	for m in range(0,len(nodes)):
		if nodes[m]=='ns5.gdnsec.com.':
			break
	print edges[n][m]
	print edges[m][n]
	edges[n][m]=9999
	edges[m][n]=9999
def find_data(data):
	if False:
		if data['sip']=='192.55.83.30':
			print data
	if False:	
		for a in data['add']:
			if find_ip(a)=='45.116.42.4':
				print data
	if False:
		for a in data['ans']:
			if find_ip(a)=='45.116.42.4':
				print data
	if True:
		for a in  data['aut']:
			if find_domain(a)=='ns4.gdnsdef.com.':
				print data
	if False:
		if data['q']=='ns5.gdnsec.com.':
			print data
def analyse_nr(filename):
	data=readjson('./resultnr/'+filename+'.json')
	nodes=[]
	nodes.append('.')
	rootip=['198.41.0.4', '192.228.79.201', '192.33.4.12', '199.7.91.13', '192.203.230.10', '192.5.5.241', '192.112.36.4', '198.97.190.53', '192.36.148.17', '192.58.128.30', '193.0.14.129', '199.7.83.42', '202.12.27.33']
	for d in data:
		addnode(nodes,d['q'].lower())
		for a in d['add']:
			domain=find_domain(a)
			addnode(nodes,domain)
		addnode(nodes,d['autname'])
		for au in d['aut']:
			domain=find_domain(au)
			addnode(nodes,domain)
		for an in d['ans']:
			domain=find_domain(an)
			addnode(nodes,domain)

	#------------------add-node-end---------------------------#
	
	edges=[]
	
	for i in range(0,len(nodes)):
		edges.append([])
		for j in range(0,len(nodes)):
			edges[i].append(0)
	#find_edge(nodes,edges)
	#start dependent on end
 	for d in data:
 		find_data(d)
		for an in d['ans']:
			start=find_domain(an)
			cname=find_cname(an)
			if cname !='':
				addedge(nodes,edges,start,cname,d,1)
			for au in d['aut']:
				end=find_domain(au)
				addedge(nodes,edges,start,end,d,2)
		for au in d['aut']:
			end=find_domain(au)
			addedge(nodes,edges,d['autname'],end,d,3)
		for add in d['add']:
			ip=find_ip(add)

			end=find_domain(add)
			for dd in data:
				if dd['sip']==ip:
					for au2 in dd['aut']:
						start=find_domain(au2)
						addedge(nodes,edges,start,end,dd,4)
					for an2 in dd['ans']:
						start=find_domain(an2)
						addedge(nodes,edges,start,end,dd,5)
	for d in data:
		end='.'
		for ip in rootip:
			if d['sip']==ip:
					for au2 in d['aut']:
						start=find_domain(au2)
						addedge(nodes,edges,start,end,d,6)
					for an2 in d['ans']:
						start=find_domain(an2)
						addedge(nodes,edges,start,end,d,7)
	#test(nodes,edges)
	#-----------------------------add-edge-end--------------#
	nodeid=[]
	for n in range(0,len(nodes)):
		isstart=0
		isend=0
		for i in range(0,len(nodes)):
			if edges[i][n]==1:
				isstart=1
				break
		if isstart==0:
			nodeid.append(10)
		else :
			for i in range(0,len(nodes)):
				if edges[n][i]==1:
					isend=1
					break
			if isend==0:
				nodeid.append(40)
			else:
				nodeid.append(100)
	#for n in range(0,len(nodes)):
	#	print nodes[n]
	#	print nodeid[n]
	draw_graph(nodes,edges,nodeid)
