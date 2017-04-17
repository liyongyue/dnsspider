import json
from analyse_dependency import draw_graph
def readjson(filename):
	with open(filename,'r') as f:
		data=json.load(f)
	return data
def analyse_nr(filename):
	domain=[]
	temp={}
	data=readjson('./resultnr/'+filename+'.json')
	temp['domain']='.'
	temp['ns']=[]
	temp['ns'].append('a.root-servers.net.')
	temp['ns'].append('b.root-servers.net.')
	temp['ns'].append('c.root-servers.net.')
	temp['ns'].append('d.root-servers.net.')
	temp['ns'].append('e.root-servers.net.')
	temp['ns'].append('f.root-servers.net.')
	temp['ns'].append('g.root-servers.net.')
	temp['ns'].append('h.root-servers.net.')
	temp['ns'].append('i.root-servers.net.')
	temp['ns'].append('j.root-servers.net.')
	temp['ns'].append('k.root-servers.net.')
	temp['ns'].append('l.root-servers.net.')
	temp['ns'].append('m.root-servers.net.')
	temp['id']=0
	domain.append(temp)
	for d in data:
		flag=0
		temp={}
		if len(d['authority'])>0:
			#print d['authority'][0]
			for dm in domain:
		 		if dm['domain']==d['authority'][0]:
					flag=1
			if flag==0:
				temp['domain']=d['authority'][0]
				temp['ns']=[]
				temp['id']=0
				for i in range(1,len(d['authority'])):
					temp['ns'].append(d['authority'][i])
				print temp['domain']
				domain.append(temp)
	edge=[]
	for i in range(0,len(domain)):
		edge.append([])
		for j in range(0,len(domain)):
			edge[i].append(0)
	for dm in domain:
		dm['edge']=[]
		for ns in dm['ns']:
			for d in data:
				if len(d['authority'])>0:
					if d['server']==ns:
						for i in range(len(domain)):
							if domain[i]['domain']==d['authority'][0]:
								flag=0
								for e in dm['edge']:
									if e==i:
										flag=1
										break
								if flag==0:
									dm['edge'].append(i)
	for ii in range(len(domain)):
		for e in domain[ii]['edge']:
			edge[ii][e]=1
	for d in domain:
		print d
	for e in edge:
		print e
	draw_graph(domain,edge)
