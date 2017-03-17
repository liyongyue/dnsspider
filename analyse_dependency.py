#coding=utf-8
import json
import networkx as nx
import matplotlib.pyplot as plt
def readjson(filename):
	with open(filename,'r') as f:
		data=json.load(f)
	return data
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
	for p in pos:
		plt.text(pos.values()[i][0],pos.values()[i][1],pos.keys()[i],horizontalalignment='center')
		i+=1
	plt.show()
if __name__=="__main__":
	target='hit.edu.cn'
	if target[-1]!='.':
		target=target+'.'
	target.lower()
	data=readjson(target+'json')
	edge=[]
	for i in range(0,len(data)):
		edge.append([])
		for j in range(0,len(data)):
			edge[i].append(0)
	for i in range(0,len(data)):
		for j in range(0,len(data)):#i->j
			if (str(data[i]['domain'])).endswith(str(data[j]['domain'])):
				edge[i][j]=1
			for ns in data[i]['ns']:
				nsstr=str(ns)
				print nsstr
				if nsstr.endswith(str(data[j]['domain'])):
					edge[i][j]=1
	for d in data :
		print d
	for i in range(0,len(data)):
		print edge[i]
	draw_graph(data,edge)
