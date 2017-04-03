#coding=utf-8
import json
import networkx as nx
import matplotlib.pyplot as plt
def readjson(filename):
	with open(filename,'r') as f:
		data=json.load(f)
	return data
class nodepos():
	def __init__(self,domain,index,ns,x,y):
		self.domain=domain
		self.ns=ns
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
		
def draw_graph(nodes,edges):
	G=nx.DiGraph()
	for n in nodes:
		G.add_node(n['domain'])
	for i in range(0,len(edges)):
		for j in range(0,len(edges)):
			if edges[i][j]==1:
				G.add_edge(nodes[i]['domain'],nodes[j]['domain'])
	pos = nx.spring_layout(G)
	nx.draw(G,pos,node_size=10000,node_color='w')
	i=0
	js=[]
	jse=[]
	for p in pos:
		plt.text(pos.values()[i][0],pos.values()[i][1],pos.keys()[i],horizontalalignment='center')
		p=nodepos(nodes[i]['domain'],nodes[i]['id'],nodes[i]['ns'],pos.values()[i][0]*200,pos.values()[i][1]*200)
		js.append(p.__dict__)
		i+=1
	json_np=json.dumps(js)
	for i in range(0,len(edges)):
		for j in range(0,len(edges)):
			if edges[i][j]==1 and edges[i][j]==edges[j][i]:
				edges[i][j]=0
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
def a_d(filename):
	data=readjson('./result/'+filename+'.json')
	edge=[]
	js=[]
	for i in range(0,len(data)):
		edge.append([])
		for j in range(0,len(data)):
			edge[i].append(0)
	for i in range(0,len(data)):
		domain=str(data[i]['domain'])
		for j in range(0,len(data)):#i->j
			if i!=j:
				odomain=str(data[j]['domain'])
				if domain.endswith(odomain) and (len(domain.split('.'))-len(odomain.split('.'))==1):
					edge[i][j]=1
					print domain
					print odomain
					continue
	#				d=depedge(i,j)
	#				js.append(d.__dict__)
				for ns in data[i]['ns']:
					nsstr=str(ns)
					#print nsstr
					if nsstr.endswith(odomain):
						if(not odomain.endswith(nsstr)) and (len(nsstr.split('.'))-len(odomain.split('.'))==1):
							edge[i][j]=1
							print domain
							print odomain
							break
					#d=depedge(i,j)
					#
#	print d
#for i in range(0,len(data)):
#	print edge[i]
#json_e=json.dumps(js)
#edgeo=open('./map/edge.json','w')
#edgeo.write(json_e)
#edgeo.close()
	draw_graph(data,edge)
