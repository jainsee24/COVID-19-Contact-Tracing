import networkx as nx 
import matplotlib.pyplot as plt 

def dijkstra(graph,src,dest,visited=[],distances={},predecessors={}):
    if src not in graph:
        return -1,-1
    if dest not in graph:
        return -1,-1    
    if src == dest:
        path=[]
        pred=dest
        while pred != None:
            path.append(pred)
            pred=predecessors.get(pred,None)
        readable=str(path[0])
        for index in range(1,len(path)): readable = str(path[index])+'--->'+readable
        cost=str(distances[dest])
        return path,cost
    else:    
        if not visited: 
            distances[src]=0
        for neighbor in graph[src] :
            if neighbor not in visited:
                new_distance = distances[src] + graph[src][neighbor]
                if new_distance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = src
        visited.append(src)
        unvisited={}
        for k in graph:
            if k not in visited:
                unvisited[k] = distances.get(k,float('inf'))        
        x=min(unvisited, key=unvisited.get)
        path,cost=dijkstra(graph,x,dest,visited,distances,predecessors)
        return path,cost

cities=['Indore','Bhopal','Chennai','Mumbai','Delhi','Bangalore','Lucknow','Hyderabad','Pune','Kolkata']

d={1: {2: 193, 4: 584, 9: 593, 5: 837, 8: 865, 7: 795}, 2: {1: 193, 5: 757, 7: 614, 10: 1433, 8: 852, 9: 783}, 4: {1: 584, 9: 148, 5: 1408}, 9: {1: 593, 4: 148, 6: 842, 8: 555, 2: 783}, 5: {1: 837, 2: 757, 4: 1408, 7: 554}, 8: {1: 865, 2: 852, 3: 626, 6: 569, 9: 555, 10: 1485}, 7: {2: 614, 5: 554, 10: 993, 1: 795}, 10: {2: 1433, 7: 993, 8: 1485}, 3: {8: 626, 6: 334}, 6: {3: 334, 8: 569, 9: 842}}
# for i in d:
# 	for j in d[i]:
# 		print(cities[i-1],cities[j-1],d[j][i])
# for i in range(len(cities)):
# 	print(i+1,cities[i])

g = nx.Graph() 
for i in d:
	for j in d[i]:
		g.add_edge(cities[i-1], cities[j-1],weight=d[i][j]) 
# drawing in circular layout 
nx.draw_circular(g, with_labels = True) 
plt.savefig("GraphWithCities.png") 
#plt.show()
plt.clf() 
hotspot=[]
hotspot=[1]

newgraph={}

for i in d:
	if i in hotspot:
		continue
	else:
		for j in d[i]:
			if j in hotspot:
				continue
			else:
				if i not in newgraph:
					newgraph[i]={}
				if j not in newgraph[i]:
					newgraph[i][j]=d[i][j]
# print(d)			
# print(newgraph)
def f(a,b):
	for i in range(0,len(a)-1):
		print(cities[a[i]-1],'-->',end='')
	print(cities[a[-1]-1])
	print('Total Cost: ',b)
source=5
destination=9
print('Without Hotspot')
a,b=dijkstra(newgraph,source,destination)
f(a,b)
print('With Hotspot')
a,b=dijkstra(d,source,destination)
f(a,b)